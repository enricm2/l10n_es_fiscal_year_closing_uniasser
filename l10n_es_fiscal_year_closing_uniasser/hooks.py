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
from odoo import api, SUPERUSER_ID


def create_default_journals(cr, registry):
    """
    Post-install hook: Creates default journals for fiscal year closing.
    
    This function creates three journals for each company:
    - REGUL: Regularization journal (for P&L accounts)
    - CIERRE: Closing journal (for balance sheet accounts)
    - APERT: Opening journal (for next fiscal year)
    
    Args:
        cr: Database cursor
        registry: Odoo registry
        
    Returns:
        bool: True when completed
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    import logging
    _logger = logging.getLogger(__name__)
    
    # Get all companies
    companies = env['res.company'].search([])
    
    for company in companies:
        # Define required journals for fiscal year closing process
        default_journals = [
            {
                'name': 'Diario Regularización',  # Regularization Journal
                'code': 'REGUL',
                'type': 'general',
                'company_id': company.id,
                'show_on_dashboard': False,
            },
            {
                'name': 'Diario Cierre',  # Closing Journal
                'code': 'CIERRE', 
                'type': 'general',
                'company_id': company.id,
                'show_on_dashboard': False,
            },
            {
                'name': 'Diario Apertura',  # Opening Journal
                'code': 'APERT',
                'type': 'general',
                'company_id': company.id,
                'show_on_dashboard': False,
            }
        ]
        
        journals_created = 0
        for journal_data in default_journals:
            # Check if journal already exists
            existing = env['account.journal'].search([
                ('code', '=', journal_data['code']),
                ('company_id', '=', company.id)
            ])
            
            if not existing:
                env['account.journal'].create(journal_data)
                journals_created += 1
        
        if journals_created > 0:
            _logger.info(
                "Created %d default journals for company %s", 
                journals_created, 
                company.name
            )
    
    return True
