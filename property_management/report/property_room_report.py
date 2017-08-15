# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-2013 Serpent Consulting Services PVT LTD (<http://www.serpentcs.com>)
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
############################################################################

from openerp.report import report_sxw

class room_property_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(room_property_report, self).__init__(cr, uid, name, context=context)   
        self.context = context

report_sxw.report_sxw('report.property.room', 'property',
        'addons/property_management/report/room_property.rml', parser=room_property_report)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: