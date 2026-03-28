# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
##############################################################################

from odoo import models, fields, api, _

class AccountFiscalyear(models.Model):
    """
    Recreamos el modelo de Año Fiscal que Odoo eliminó, para poder 
    gestionar los cierres legales en España de forma organizada.
    """
    _name = "account.fiscalyear"
    _description = "Año Fiscal (Compatibilidad Cierre)"

    name = fields.Char(string='Año Fiscal', required=True)
    code = fields.Char(string='Código', size=6, required=True)
    company_id = fields.Many2one(
        'res.company', 
        string='Compañía', 
        required=True, 
        default=lambda self: self.env.company
    )
    date_start = fields.Date(string='Fecha Inicio', required=True)
    date_stop = fields.Date(string='Fecha Fin', required=True)
    state = fields.Selection([
        ('draft', 'Abierto'),
        ('done', 'Cerrado')
    ], string='Estado', default='draft', readonly=True)

    @api.model
    def create_period(self, interval=1):
        """
        Adaptación de la lógica de Odoo 8 para generar periodos.
        En Odoo 19, esto servirá para marcar los rangos de fechas
        de los asientos de regularización y cierre.
        """
        for fy in self:
            # En Odoo 19 no existen los objetos account.period, 
            # así que gestionamos la lógica mediante metadatos en el cierre.
            pass
        return True

class AccountMove(models.Model):
    _inherit = "account.move"

    # Añadimos un campo para identificar si el asiento es de un cierre fiscal
    fyc_type = fields.Selection([
        ('lp', 'Pérdidas y Ganancias'),
        ('close', 'Cierre'),
        ('open', 'Apertura')
    ], string='Tipo de Cierre Fiscal', readonly=True)