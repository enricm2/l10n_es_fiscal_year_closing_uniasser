# -*- coding: utf-8 -*-
{
    'name': 'Spanish Fiscal Year Closing',
    'version': '18.0.1.0.0',
    'summary': 'Cierre de Ejercicio Fiscal según normativa española (PGC)',
    'description': """
        Spanish Fiscal Year Closing - Cierre de Ejercicio Fiscal
        ==========================================================
        
        Este módulo permite realizar el cierre de ejercicio fiscal según la 
        normativa contable española (Plan General Contable - PGC).
        
        Características principales:
        ----------------------------
        * Asiento de Regularización (Diario REGUL): Regulariza cuentas de PyG
        * Asiento de Cierre (Diario CIERRE): Cierra el balance
        * Asiento de Apertura (Diario APERT): Abre el nuevo ejercicio
        * Gestión automática de diarios
        * Proceso reversible y seguro
        * Seguimiento completo con chatter
        * Soporte multi-compañía
        
        Cumple con el Plan General Contable español:
        --------------------------------------------
        * Regularización de grupos 6 y 7 contra cuenta 129
        * Cierre de cuentas de balance (grupos 1-5)
        * Apertura automática del nuevo ejercicio
        
        Para más información, consulte el README.rst
    """,
    'author': 'Uniasser Consulting SL, Enric J. Marti Albella',
    'website': 'https://www.uniasser.com',
    'category': 'Accounting/Localizations/Account Charts',
    'license': 'LGPL-3',
    'price': 79.00,
    'currency': 'EUR',
    'depends': [
        'base',
        'account',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/fiscalyear_closing_view.xml',
        'wizard/wizard_run_view.xml',
    ],
    'images': [
        'static/description/icon.png',
        'static/description/screenshot_01.png',
        'static/description/screenshot_02.png',
        'static/description/screenshot_03.png',
        'static/description/screenshot_04.png',
        'static/description/screenshot_05.png',
        'static/description/screenshot_06.png',
    ],
    'post_init_hook': 'create_default_journals',
    'installable': True,
    'application': True,
    'auto_install': False,
    'support': 'info@uniasser.com',
    'maintainer': 'Uniasser Consulting SL',
    'contributors': [
        'Enric J. Marti Albella <enric@uniasser.com>',
    ],
}
