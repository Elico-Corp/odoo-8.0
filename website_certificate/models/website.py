# © 2015-2019 Elico corp (www.elico-corp.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import models, fields


class Website(models.Model):
    _inherit = 'website'

    certificate_number1 = fields.Char(string='Certificate Number1')
    certificate_number1_url = fields.Char(string='Certificate Number1 URL')
    certificate_url1 = fields.Char(string='Certificate URL1')
    certificate_logo1 = fields.Binary(string='Certificate Logo1')
    certificate_number2 = fields.Char(string='Certificate Number2')
    certificate_url2 = fields.Char(string='Certificate URL2')
    certificate_logo2 = fields.Binary(string='Certificate Logo2')
