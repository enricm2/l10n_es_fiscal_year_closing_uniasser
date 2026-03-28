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
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class FiscalyearClosingRun(models.TransientModel):
    """
    Asistente para la ejecución técnica de los asientos de cierre.
    Este modelo procesa los saldos y genera los movimientos contables.
    """
    _name = "account.fiscalyear.closing.run"
    _description = "Ejecutor de Asientos de Cierre Fiscal"

    fyc_id = fields.Many2one(
        'account.fiscalyear.closing', 
        string='Configuración de Cierre', 
        required=True,
        ondelete='cascade'
    )

    def _get_move_lines(self, account_ids, date_start, date_stop, company_id):
        """
        Consulta SQL de bajo nivel para obtener saldos netos por cuenta.
        Garantiza eficiencia en bases de datos con gran volumen.
        """
        query = """
            SELECT account_id, SUM(debit) as debit, SUM(credit) as credit, SUM(debit - credit) as balance
            FROM account_move_line
            WHERE date >= %s AND date <= %s 
              AND company_id = %s 
              AND parent_state = 'posted'
              AND account_id IN %s
            GROUP BY account_id
            HAVING SUM(debit - credit) != 0
        """
        self.env.cr.execute(query, (date_start, date_stop, company_id, tuple(account_ids)))
        return self.env.cr.dictfetchall()

    def create_closing_asientos(self):
        """
        MÉTODO PRINCIPAL: Ejecuta la secuencia legal de cierre.
        """
        self.ensure_one()
        fyc = self.fyc_id
        
        if fyc.state != 'calculated':
            raise UserError(_("El cierre debe estar en estado 'Calculado' para generar los asientos."))

        # 1. PASO: ASIENTO DE REGULARIZACIÓN (DIARIO REGUL)
        # ---------------------------------------------------------------------
        if fyc.create_loss_and_profit and not fyc.lp_move_id:
            _logger.info("Generando asiento de Regularización (PyG)...")
            
            # Buscamos cuentas de ingresos y gastos (Grupos 6 y 7)
            pyg_accounts = self.env['account.account'].search([
                ('company_id', '=', fyc.company_id.id),
                '|', ('code', '=like', '6%'), ('code', '=like', '7%')
            ])
            
            if not pyg_accounts:
                raise UserError(_("No se han encontrado cuentas de los grupos 6 o 7 para regularizar."))

            saldos = self._get_move_lines(pyg_accounts.ids, fyc.date_start, fyc.date_stop, fyc.company_id.id)
            
            if saldos:
                line_ids = []
                total_balance = 0.0
                
                for line in saldos:
                    balance = line['balance']
                    total_balance += balance
                    line_ids.append((0, 0, {
                        'name': _('Regularización de existencias e ingresos/gastos'),
                        'account_id': line['account_id'],
                        'debit': abs(balance) if balance < 0 else 0.0,
                        'credit': balance if balance > 0 else 0.0,
                    }))
                
                # Contrapartida a la cuenta 129
                acc_129 = self.env['account.account'].search([
                    ('code', '=', '129'), 
                    ('company_id', '=', fyc.company_id.id)
                ], limit=1)
                
                if not acc_129:
                    raise UserError(_("No existe la cuenta 129 (Resultado del Ejercicio) en su plan contable."))

                line_ids.append((0, 0, {
                    'name': _('Resultado del Ejercicio (Cuenta 129)'),
                    'account_id': acc_129.id,
                    'debit': total_balance if total_balance > 0 else 0.0,
                    'credit': abs(total_balance) if total_balance < 0 else 0.0,
                }))

                move_pyg = self.env['account.move'].create({
                    'journal_id': fyc.lp_journal_id.id,
                    'date': fyc.date_stop,
                    'ref': f"REGUL - {fyc.name}",
                    'move_type': 'entry',
                    'line_ids': line_ids,
                })
                move_pyg.action_post()
                fyc.lp_move_id = move_pyg.id

        # 2. PASO: ASIENTO DE CIERRE (DIARIO CIERRE)
        # ---------------------------------------------------------------------
        if fyc.create_closing and not fyc.closing_move_id:
            _logger.info("Generando asiento de Cierre de Balance...")
            
            # Buscamos todas las cuentas con saldo (excepto 6 y 7 que ya están a cero)
            balance_accounts = self.env['account.account'].search([
                ('company_id', '=', fyc.company_id.id),
                ('code', 'not like', '6%'),
                ('code', 'not like', '7%')
            ])
            
            saldos_balance = self._get_move_lines(balance_accounts.ids, fyc.date_start, fyc.date_stop, fyc.company_id.id)
            
            if saldos_balance:
                c_line_ids = []
                for line in saldos_balance:
                    balance = line['balance']
                    c_line_ids.append((0, 0, {
                        'name': _('Asiento de cierre de ejercicio'),
                        'account_id': line['account_id'],
                        'debit': abs(balance) if balance < 0 else 0.0,
                        'credit': balance if balance > 0 else 0.0,
                    }))
                
                move_close = self.env['account.move'].create({
                    'journal_id': fyc.closing_journal_id.id,
                    'date': fyc.date_stop,
                    'ref': f"CIERRE - {fyc.name}",
                    'move_type': 'entry',
                    'line_ids': c_line_ids,
                })
                move_close.action_post()
                fyc.closing_move_id = move_close.id

        # 3. PASO: ASIENTO DE APERTURA (DIARIO APERTURA)
        # ---------------------------------------------------------------------
        if fyc.create_opening and fyc.closing_move_id and not fyc.opening_move_id:
            _logger.info("Generando asiento de Apertura...")
            
            o_line_ids = []
            # La apertura es el inverso exacto de las líneas del asiento de cierre
            for line in fyc.closing_move_id.line_ids:
                o_line_ids.append((0, 0, {
                    'name': _('Asiento de apertura de ejercicio'),
                    'account_id': line.account_id.id,
                    'partner_id': line.partner_id.id,
                    'debit': line.credit,
                    'credit': line.debit,
                }))
                
            move_open = self.env['account.move'].create({
                'journal_id': fyc.opening_journal_id.id,
                'date': fyc.date_opening,
                'ref': f"APERT - {fyc.name}",
                'move_type': 'entry',
                'line_ids': o_line_ids,
            })
            move_open.action_post()
            fyc.opening_move_id = move_open.id

        fyc.write({'state': 'done'})
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Proceso finalizado'),
                'message': _('Se han generado y validado los 3 asientos en sus diarios correspondientes.'),
                'type': 'success',
                'sticky': False,
            }
        }

class CancelFycWizard(models.TransientModel):
    """
    Asistente para revertir el cierre de forma segura.
    """
    _name = "account.fiscalyear.closing.cancel_wizard"
    _description = "Asistente de Cancelación de Cierre"

    confirm = fields.Boolean(string="Confirmo que deseo eliminar los asientos de cierre", default=False)

    def run_cancel(self):
        self.ensure_one()
        if not self.confirm:
            raise UserError(_("Debe marcar la casilla de confirmación para continuar."))
            
        active_id = self.env.context.get('active_id')
        fyc = self.env['account.fiscalyear.closing'].browse(active_id)
        
        if fyc:
            # Llamamos al método de reversión definido en el modelo principal
            fyc.action_cancel_draft()
            
        return {'type': 'ir.actions.act_window_close'}