# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010-2015 Elico Corp (<http://www.elico-corp.com>)
#    Authors: Rona Lin
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Website Header Language Switch',
    'version': '8.0.0.0.2',
    'category': 'website',
    'depends': ['base', 'website'],
    'author': 'Elico-Corp,Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'https://www.elico-corp.com',
    'images': [],
    'demo': [],
    'data': ['header_language.xml'],
    'installable': True,
    'application': False,
    'description': """
         Add a language switch in the header of the website.
    """
}
