# -*- coding: utf-8 -*-
##############################################################################
#
#    Spanish Fiscal Year Closing
#    Copyright (C) 2024-2025 Uniasser Consulting SL
#    Author: Enric J. Marti Albella <enric@uniasser.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
##############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)

class FiscalyearClosing(models.Model):
    _name = "account.fiscalyear.closing"
    _description = "Cierre de Ejercicio Fiscal Español"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "date_stop desc"

    name = fields.Char(
        string='Descripción', 
        required=True, 
        tracking=True,
        help="Nombre identificativo del cierre, ej: Cierre Ejercicio 2024"
    )
    company_id = fields.Many2one(
        'res.company', 
        string='Compañía', 
        required=True, 
        default=lambda self: self.env.company
    )
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('calculated', 'Calculado'),
        ('done', 'Realizado'),
        ('cancelled', 'Cancelado')
    ], string='Estado', default='draft', readonly=True, tracking=True)

    # Configuración de Fechas
    date_start = fields.Date(
        string='Fecha Inicio Ejercicio', 
        required=True,
        help="Primer día del año fiscal a cerrar"
    )
    date_stop = fields.Date(
        string='Fecha Fin Ejercicio', 
        required=True,
        help="Último día del año fiscal (fecha de los asientos de cierre)"
    )
    date_opening = fields.Date(
        string='Fecha Apertura Siguiente', 
        required=True,
        help="Primer día del ejercicio siguiente (fecha del asiento de apertura)"
    )
    
    # Configuración de Diarios Específicos
    lp_journal_id = fields.Many2one(
        'account.journal', 
        string='Diario Regularización (REGUL)', 
        required=True,
        domain=[('type', '=', 'general')],
        default=lambda self: self._default_journal('REGUL')
    )
    closing_journal_id = fields.Many2one(
        'account.journal', 
        string='Diario de Cierre (CIERRE)', 
        required=True,
        domain=[('type', '=', 'general')],
        default=lambda self: self._default_journal('CIERRE')
    )
    opening_journal_id = fields.Many2one(
        'account.journal', 
        string='Diario de Apertura (APERT)', 
        required=True,
        domain=[('type', '=', 'general')],
        default=lambda self: self._default_journal('APERT')
    )
    
    # Asientos generados (Relaciones)
    lp_move_id = fields.Many2one(
        'account.move', 
        string='Asiento de Regularización', 
        readonly=True,
        ondelete='set null'
    )
    closing_move_id = fields.Many2one(
        'account.move', 
        string='Asiento de Cierre', 
        readonly=True,
        ondelete='set null'
    )
    opening_move_id = fields.Many2one(
        'account.move', 
        string='Asiento de Apertura', 
        readonly=True,
        ondelete='set null'
    )

    # Opciones de ejecución
    create_loss_and_profit = fields.Boolean(string='Generar Regularización (6 y 7)', default=True)
    create_closing = fields.Boolean(string='Generar Asiento de Cierre', default=True)
    create_opening = fields.Boolean(string='Generar Asiento de Apertura', default=True)

    # Cuenta PyG específica para España
    pyg_account_id = fields.Many2one(
        'account.account',
        string='Cuenta PyG (129)',
        required=True,
        domain=[('code', '=like', '129%')],
        help="Cuenta de Resultado del Ejercicio",
        default=lambda self: self._default_pyg_account()
    )

    @api.model
    def _default_journal(self, journal_code):
        """
        Obtiene el diario por defecto según el código.
        """
        journal = self.env['account.journal'].search([
            ('code', '=', journal_code),
            ('company_id', '=', self.env.company.id)
        ], limit=1)
        return journal.id if journal else False

    @api.model
    def _default_pyg_account(self):
        """Obtener la cuenta PyG por defecto (cuenta 129)"""
        account = self.env['account.account'].search([
            ('code_store', '=like', '129%')
        ], limit=1)
        return account.id if account else False

    @api.model_create_multi
    def create(self, vals_list):
        """
        Crear registros y asegurar que existan los diarios necesarios.
        Compatible con batch operations de Odoo 18.
        """
        # Crear diarios por defecto si no existen para cada compañía
        companies = set()
        for vals in vals_list:
            company_id = vals.get('company_id', self.env.company.id)
            companies.add(company_id)
            self._create_default_journals(company_id)
        
        # Asignar diarios por defecto si no se especifican
        for vals in vals_list:
            company_id = vals.get('company_id', self.env.company.id)
            
            if not vals.get('lp_journal_id'):
                regul_journal = self.env['account.journal'].search([
                    ('code', '=', 'REGUL'),
                    ('company_id', '=', company_id)
                ], limit=1)
                if regul_journal:
                    vals['lp_journal_id'] = regul_journal.id
                    
            if not vals.get('closing_journal_id'):
                closing_journal = self.env['account.journal'].search([
                    ('code', '=', 'CIERRE'),
                    ('company_id', '=', company_id)
                ], limit=1)
                if closing_journal:
                    vals['closing_journal_id'] = closing_journal.id
                    
            if not vals.get('opening_journal_id'):
                opening_journal = self.env['account.journal'].search([
                    ('code', '=', 'APERT'),
                    ('company_id', '=', company_id)
                ], limit=1)
                if opening_journal:
                    vals['opening_journal_id'] = opening_journal.id
        
        return super(FiscalyearClosing, self).create(vals_list)

    @api.model
    def _create_default_journals(self, company_id):
        """
        Crea los diarios por defecto si no existen (método interno).
        """
        journals_to_create = []
        
        default_journals = [
            {
                'name': 'Diario Regularización',
                'code': 'REGUL',
                'type': 'general',
                'company_id': company_id,
                'show_on_dashboard': False,
            },
            {
                'name': 'Diario Cierre',
                'code': 'CIERRE', 
                'type': 'general',
                'company_id': company_id,
                'show_on_dashboard': False,
            },
            {
                'name': 'Diario Apertura',
                'code': 'APERT',
                'type': 'general',
                'company_id': company_id,
                'show_on_dashboard': False,
            }
        ]
        
        for journal_data in default_journals:
            existing = self.env['account.journal'].search([
                ('code', '=', journal_data['code']),
                ('company_id', '=', company_id)
            ])
            
            if not existing:
                journals_to_create.append(journal_data)
        
        if journals_to_create:
            created_journals = self.env['account.journal'].create(journals_to_create)
            _logger.info(f"Creados {len(created_journals)} diarios por defecto para la compañía {company_id}")

    @api.onchange('date_stop')
    def _onchange_date_stop(self):
        """Sugiere el día siguiente como fecha de apertura"""
        if self.date_stop:
            self.date_opening = self.date_stop + timedelta(days=1)

    def action_calculate(self):
        """Valida que no haya problemas previos al cierre."""
        for record in self:
            # 1. Comprobar asientos descuadrados
            record._check_unbalanced_moves()
            # 2. Comprobar si hay asientos en borrador
            record._check_draft_moves()
            
            record.write({'state': 'calculated'})
        return True

    def _check_unbalanced_moves(self):
        """Verifica descuadres por SQL para máxima precisión."""
        self.env.cr.execute("""
            SELECT move_id FROM account_move_line 
            WHERE company_id = %s AND date >= %s AND date <= %s AND parent_state = 'posted'
            GROUP BY move_id HAVING ABS(SUM(debit) - SUM(credit)) > 0.0001
        """, (self.company_id.id, self.date_start, self.date_stop))
        if self.env.cr.fetchall():
            raise UserError(_("Se han detectado asientos descuadrados en el ejercicio. Por favor, revíselos antes de continuar."))

    def _check_draft_moves(self):
        """Verifica que no queden asientos sin asentar."""
        draft_moves = self.env['account.move'].search_count([
            ('company_id', '=', self.company_id.id),
            ('date', '>=', self.date_start),
            ('date', '<=', self.date_stop),
            ('state', '=', 'draft')
        ])
        if draft_moves > 0:
            raise UserError(_("Existen %s asientos en estado borrador. Debe publicarlos o eliminarlos.") % draft_moves)

    def action_cancel_draft(self):
        """
        REVERSIÓN TOTAL DEL CIERRE.
        Busca los 3 asientos, los pasa a borrador y los borra.
        """
        for record in self:
            moves_to_remove = self.env['account.move']
            if record.lp_move_id: moves_to_remove |= record.lp_move_id
            if record.closing_move_id: moves_to_remove |= record.closing_move_id
            if record.opening_move_id: moves_to_remove |= record.opening_move_id
            
            for move in moves_to_remove:
                if move.state == 'posted':
                    move.button_draft()
                # Forzamos borrado incluso si el diario tiene secuencia
                move.with_context(force_delete=True).unlink()
            
            record.write({
                'state': 'draft', 
                'lp_move_id': False, 
                'closing_move_id': False, 
                'opening_move_id': False
            })
        return True

    def unlink(self):
        for record in self:
            if record.state != 'draft':
                raise UserError(_("No puede eliminar un cierre que no esté en borrador."))
        return super(FiscalyearClosing, self).unlink()

    def run_closing_process(self):
        """Ejecución integral: PyG -> Cierre -> Apertura"""
        self.ensure_one()
        
        if not self.date_opening:
            raise UserError(_("Debe definir la fecha de apertura (ej: 01/01 del año siguiente)."))

        # 1. ASIENTO DE REGULARIZACIÓN (PYG - GRUPOS 6 Y 7)
        if not self.lp_move_id:
            lines = self._prepare_pyg_lines()
            if lines:
                # Logging detallado antes de crear
                total_debit = sum(line[2].get('debit', 0.0) for line in lines)
                total_credit = sum(line[2].get('credit', 0.0) for line in lines)
                
                _logger.info(f"=== CREANDO ASIENTO DE REGULARIZACIÓN ===")
                _logger.info(f"Líneas a crear: {len(lines)}")
                _logger.info(f"Total débito: {total_debit}")
                _logger.info(f"Total crédito: {total_credit}")
                _logger.info(f"Diferencia: {total_debit - total_credit}")
                
                # Verificar balance antes de crear
                if abs(total_debit - total_credit) > 0.000001:
                    _logger.error(f"ERROR: Asiento descuadrado antes de crear - débito={total_debit}, crédito={total_credit}")
                    raise UserError(_("El asiento de regularización está descuadrado. Débito: %s, Crédito: %s") % (total_debit, total_credit))
                
                move_vals = self._prepare_move_vals(self.lp_journal_id, self.date_stop, _("Regularización PyG"))
                move_vals['line_ids'] = lines
                
                _logger.info(f"move_vals completos: {move_vals}")
                
                try:
                    self.lp_move_id = self.env['account.move'].create(move_vals)
                    _logger.info("Asiento de regularización creado: %s", self.lp_move_id.name)
                    self.lp_move_id.action_post()
                    _logger.info("Asiento de regularización publicado: %s", self.lp_move_id.name)
                except Exception as e:
                    _logger.error(f"Error creando asiento: {e}")
                    raise

        # 2. ASIENTO DE CIERRE (CIERRE DE CUENTAS DE BALANCE)
        if not self.closing_move_id:
            lines = self._prepare_closing_lines()
            if lines:
                # Logging detallado para asiento de cierre
                total_debit = sum(line[2].get('debit', 0.0) for line in lines)
                total_credit = sum(line[2].get('credit', 0.0) for line in lines)
                
                _logger.info(f"=== CREANDO ASIENTO DE CIERRE ===")
                _logger.info(f"Líneas a crear: {len(lines)}")
                _logger.info(f"Total débito: {total_debit}")
                _logger.info(f"Total crédito: {total_credit}")
                _logger.info(f"Diferencia: {total_debit - total_credit}")
                
                # Verificar balance antes de crear
                if abs(total_debit - total_credit) > 0.000001:
                    _logger.error(f"ERROR: Asiento de cierre descuadrado - débito={total_debit}, crédito={total_credit}")
                    raise UserError(_("El asiento de cierre está descuadrado. Débito: %s, Crédito: %s") % (total_debit, total_credit))
                
                move_vals = self._prepare_move_vals(self.closing_journal_id, self.date_stop, _("Cierre de Ejercicio"))
                move_vals['line_ids'] = lines
                
                _logger.info(f"move_vals de cierre completos: {move_vals}")
                
                try:
                    self.closing_move_id = self.env['account.move'].create(move_vals)
                    _logger.info("Asiento de cierre creado: %s", self.closing_move_id.name)
                    self.closing_move_id.action_post()
                    _logger.info("Asiento de cierre publicado: %s", self.closing_move_id.name)
                except Exception as e:
                    _logger.error(f"Error creando asiento de cierre: {e}")
                    raise

        # 3. ASIENTO DE APERTURA (APERTURA DEL SIGUIENTE EJERCICIO)
        if not self.opening_move_id:
            lines = self._prepare_opening_lines()
            if lines:
                move_vals = self._prepare_move_vals(self.opening_journal_id, self.date_opening, _("Apertura de Ejercicio"))
                move_vals['line_ids'] = lines
                self.opening_move_id = self.env['account.move'].create(move_vals)
                self.opening_move_id.action_post()
                _logger.info("Asiento de apertura creado: %s", self.opening_move_id.name)

        self.write({'state': 'done'})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Cierre Completado'),
                'message': _('Proceso de cierre finalizado correctamente.'),
                'type': 'success',
            }
        }

    def _prepare_pyg_lines(self):
        """Prepara las líneas para el asiento de regularización PyG"""
        lines = []
        _logger.info("=== INICIANDO PREPARACIÓN DE LÍNEAS PyG ===")
        
        # Obtener cuentas de ingresos y gastos (Grupos 6 y 7)
        pyg_accounts = self.env['account.account'].search([
            '|', ('code_store', '=like', '6%'), ('code_store', '=like', '7%')
        ])
        
        _logger.info(f"Cuentas PyG encontradas: {len(pyg_accounts)}")
        
        if not pyg_accounts:
            raise UserError(_("No se han encontrado cuentas de los grupos 6 o 7 para regularizar."))

        # Consulta SQL para obtener saldos con máxima precisión
        query = """
            SELECT account_id, SUM(debit - credit) as balance
            FROM account_move_line
            WHERE date >= %s AND date <= %s 
              AND company_id = %s 
              AND parent_state = 'posted'
              AND account_id IN %s
            GROUP BY account_id
            HAVING ABS(SUM(debit - credit)) > 0.000001
        """
        self.env.cr.execute(query, (self.date_start, self.date_stop, self.company_id.id, tuple(pyg_accounts.ids)))
        saldos = self.env.cr.dictfetchall()
        
        _logger.info(f"Saldos encontrados: {len(saldos)}")
        
        # Construir líneas con valores exactos
        total_debit = 0.0
        total_credit = 0.0
        
        for saldo in saldos:
            balance = float(saldo['balance'])
            _logger.info(f"Cuenta {saldo['account_id']}: balance = {balance}")
            
            if abs(balance) > 0.000001:  # Solo incluir si hay saldo significativo
                if balance > 0:
                    line_data = {
                        'name': _('Regularización de existencias e ingresos/gastos'),
                        'account_id': saldo['account_id'],
                        'debit': balance,
                        'credit': 0.0,
                    }
                    lines.append((0, 0, line_data))
                    total_debit += balance
                    _logger.info(f"Línea débito: cuenta={saldo['account_id']}, amount={balance}")
                else:
                    line_data = {
                        'name': _('Regularización de existencias e ingresos/gastos'),
                        'account_id': saldo['account_id'],
                        'debit': 0.0,
                        'credit': abs(balance),
                    }
                    lines.append((0, 0, line_data))
                    total_credit += abs(balance)
                    _logger.info(f"Línea crédito: cuenta={saldo['account_id']}, amount={abs(balance)}")
        
        _logger.info(f"Totales antes de contrapartida: débito={total_debit}, crédito={total_credit}")
        _logger.info(f"Diferencia: {total_debit - total_credit}")
        
        # Contrapartida a la cuenta 129 - Asegurar balance perfecto
        if lines and abs(total_debit - total_credit) > 0.000001:
            # Calcular la diferencia exacta para balancear
            difference = total_debit - total_credit
            
            _logger.info(f"Añadiendo contrapartida: diferencia={difference}")
            
            # CORRECCIÓN: Si débito > crédito, la contrapartida va a crédito
            # Si crédito > débito, la contrapartida va a débito
            if difference > 0:  # Hay más débito que crédito, añadir crédito
                lines.append((0, 0, {
                    'name': _('Resultado del Ejercicio'),
                    'account_id': self.pyg_account_id.id,
                    'debit': 0.0,
                    'credit': difference,
                }))
                _logger.info(f"Contrapartida crédito: {difference}")
            else:  # Hay más crédito que débito, añadir débito
                lines.append((0, 0, {
                    'name': _('Resultado del Ejercicio'),
                    'account_id': self.pyg_account_id.id,
                    'debit': abs(difference),
                    'credit': 0.0,
                }))
                _logger.info(f"Contrapartida débito: {abs(difference)}")
            
            # Recalcular totales finales
            final_debit = total_debit + (0.0 if difference > 0 else abs(difference))
            final_credit = total_credit + (difference if difference > 0 else 0.0)
            
            _logger.info(f"Totales finales: débito={final_debit}, crédito={final_credit}")
            _logger.info(f"Diferencia final: {final_debit - final_credit}")
        else:
            _logger.info("No se necesita contrapartida - asiento ya balanceado")
        
        _logger.info(f"Total líneas generadas: {len(lines)}")
        _logger.info("=== FIN PREPARACIÓN DE LÍNEAS PyG ===")
        
        return lines

    def _prepare_closing_lines(self):
        """Prepara las líneas para el asiento de cierre"""
        _logger.info("=== INICIANDO PREPARACIÓN DE LÍNEAS DE CIERRE ===")
        lines = []
        
        # Obtener cuentas de balance (no PyG)
        balance_accounts = self.env['account.account'].search([
            ('code_store', 'not like', '6%'),
            ('code_store', 'not like', '7%'),
            ('code_store', 'not like', '129%'),
        ])
        
        _logger.info(f"Cuentas de balance encontradas: {len(balance_accounts)}")
        
        if not balance_accounts:
            return lines

        # Consulta SQL para obtener saldos
        query = """
            SELECT account_id, SUM(debit - credit) as balance
            FROM account_move_line
            WHERE date >= %s AND date <= %s 
              AND company_id = %s 
              AND parent_state = 'posted'
              AND account_id IN %s
            GROUP BY account_id
            HAVING ABS(SUM(debit - credit)) > 0.000001
        """
        self.env.cr.execute(query, (self.date_start, self.date_stop, self.company_id.id, tuple(balance_accounts.ids)))
        saldos = self.env.cr.dictfetchall()
        
        _logger.info(f"Saldos de cierre encontrados: {len(saldos)}")
        
        # Construir líneas con valores exactos
        total_debit = 0.0
        total_credit = 0.0
        
        for saldo in saldos:
            balance = float(saldo['balance'])
            _logger.info(f"Cuenta {saldo['account_id']}: balance = {balance}")
            
            if abs(balance) > 0.000001:  # Solo incluir si hay saldo significativo
                if balance > 0:
                    lines.append((0, 0, {
                        'name': _('Cierre de cuenta'),
                        'account_id': saldo['account_id'],
                        'debit': 0.0,  # Cerrar al crédito
                        'credit': balance,
                    }))
                    total_credit += balance
                    _logger.info(f"Línea crédito: cuenta={saldo['account_id']}, amount={balance}")
                else:
                    lines.append((0, 0, {
                        'name': _('Cierre de cuenta'),
                        'account_id': saldo['account_id'],
                        'debit': abs(balance),  # Cerrar al débito
                        'credit': 0.0,
                    }))
                    total_debit += abs(balance)
                    _logger.info(f"Línea débito: cuenta={saldo['account_id']}, amount={abs(balance)}")
        
        _logger.info(f"Totales antes de contrapartida: débito={total_debit}, crédito={total_credit}")
        _logger.info(f"Diferencia: {total_debit - total_credit}")
        
        # Contrapartida a la cuenta 129 - Asegurar balance perfecto
        if lines and abs(total_debit - total_credit) > 0.000001:
            # Calcular la diferencia exacta para balancear
            difference = total_debit - total_credit
            
            _logger.info(f"Añadiendo contrapartida de cierre: diferencia={difference}")
            
            # CORRECCIÓN: Si débito > crédito, la contrapartida va a crédito
            # Si crédito > débito, la contrapartida va a débito
            if difference > 0:  # Hay más débito que crédito, añadir crédito
                lines.append((0, 0, {
                    'name': _('Resultado del Ejercicio - Cierre'),
                    'account_id': self.pyg_account_id.id,
                    'debit': 0.0,
                    'credit': difference,
                }))
                _logger.info(f"Contrapartida crédito: {difference}")
            else:  # Hay más crédito que débito, añadir débito
                lines.append((0, 0, {
                    'name': _('Resultado del Ejercicio - Cierre'),
                    'account_id': self.pyg_account_id.id,
                    'debit': abs(difference),
                    'credit': 0.0,
                }))
                _logger.info(f"Contrapartida débito: {abs(difference)}")
            
            # Recalcular totales finales
            final_debit = total_debit + (0.0 if difference > 0 else abs(difference))
            final_credit = total_credit + (difference if difference > 0 else 0.0)
            
            _logger.info(f"Totales finales: débito={final_debit}, crédito={final_credit}")
            _logger.info(f"Diferencia final: {final_debit - final_credit}")
        else:
            _logger.info("No se necesita contrapartida - asiento de cierre ya balanceado")
        
        _logger.info(f"Total líneas de cierre generadas: {len(lines)}")
        _logger.info("=== FIN PREPARACIÓN DE LÍNEAS DE CIERRE ===")
        
        return lines

    def _prepare_opening_lines(self):
        """Prepara las líneas para el asiento de apertura"""
        lines = []
        
        if not self.closing_move_id:
            return lines
        
        # Copiar las líneas del asiento de cierre invirtiendo los importes
        for line in self.closing_move_id.line_ids:
            lines.append((0, 0, {
                'name': _('Apertura de cuenta'),
                'account_id': line.account_id.id,
                'debit': line.credit,
                'credit': line.debit,
            }))
        
        return lines

    def _prepare_move_vals(self, journal_id, date, ref):
        """Prepara los valores básicos para un asiento"""
        _logger.info(f"Preparando valores para asiento: journal_id={journal_id.id}, date={date}, ref={ref}")
        return {
            'journal_id': journal_id.id,
            'date': date,
            'ref': ref,
            'company_id': self.company_id.id,
            'move_type': 'entry',
        }
