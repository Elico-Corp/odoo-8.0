# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Today Serpent Consulting Services Pvt. Ltd. 
#                                      (<http://www.serpentcs.com>)
#    Copyright (C) 2004 OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from openerp import api, models, fields
import datetime
import openerp
from openerp.http import request
from dateutil.relativedelta import relativedelta
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from openerp.tools.translate import _
from openerp import SUPERUSER_ID

_old_create = models.BaseModel.create
_old_write = models.BaseModel.write
_old_unlink = models.BaseModel.unlink

@api.model
@api.returns('self', lambda value: value.id)
def _create_method(self, vals):
    popup_obj = self.pool.get('popup.reminder')
    if popup_obj:
        model_ids = popup_obj.search(self._cr, self._uid, [('model_id','=', str(self._model))])
        res_id = False
        notifications = []
        if model_ids or str(self._model) == "popup.reminder":
            res_id = _old_create(self, vals)
            count = popup_obj.set_notification(self._cr, self._uid, True)
            notifications.append([(request.db,'popup.reminder'), count])
            self.pool['bus.bus'].sendmany(self._cr, self._uid, notifications)
            return res_id
        return _old_create(self, vals)
    return _old_create(self, vals)

models.BaseModel.create = _create_method

@api.multi
def _write_method(self, vals):
    popup_obj = self.pool.get('popup.reminder')
    if popup_obj:
        model_ids = popup_obj.search(self._cr, self._uid, [('model_id','=', str(self._model))])
        res_id = False
        notifications = []
        if model_ids or str(self._model) == "popup.reminder":
            res_id = _old_write(self, vals)
            count = popup_obj.set_notification(self._cr, self._uid, True)
            notifications.append([(request.db,'popup.reminder'), count])
            self.pool['bus.bus'].sendmany(self._cr, self._uid, notifications)
            return res_id
        else:
            return _old_write(self, vals)
    return _old_write(self, vals)

models.BaseModel.write = _write_method

def _unlink_method(self, cr, uid, ids, context=None):
    popup_obj = self.pool.get('popup.reminder')
    if popup_obj:
        model_ids = popup_obj.search(cr, uid, [('model_id','=', str(self._model))])
        res_id = False
        notifications = []
        if model_ids or str(self._model) == "popup.reminder":
            res_id = _old_unlink(self, cr, uid, ids, context=context)
            count = popup_obj.set_notification(cr, uid, True)
            notifications.append([(request.db,'popup.reminder'), count])
            self.pool['bus.bus'].sendmany(cr, uid, notifications)
            return res_id
        else:
            return _old_unlink(self, cr, uid, ids, context=context)
    return _old_unlink(self, cr, uid, ids, context=context)

models.BaseModel.unlink = _unlink_method

class Controller(openerp.addons.bus.bus.Controller):
    def _poll(self, dbname, channels, last, options):
        if request.session.uid:
            registry, cr, uid, context = request.registry, request.cr, request.session.uid, request.context
            channels.append((request.db,'popup.reminder'))
        poll = super(Controller, self)._poll(dbname, channels, last, options)
        return poll

class popup_reminder(models.Model):
    _name = 'popup.reminder'

    def get_model_name(self, cr, uid, data, context=None):
        data_ids = self.search(cr, uid, [('name','=', data)])
        model_list = []
        if data_ids:
            model_name = self.browse(cr, uid, data_ids[0]).model_id.name
            model_name1 = self.browse(cr, uid, data_ids[0]).model_id.model
            model_list.append(model_name)
            model_list.append(model_name1)
        return model_list

    def get_form_data(self, cr, uid, data, context=None):
        data_ids = self.search(cr, uid, [('name','=', data)])
        model_name = ''
        if data_ids:
            model_name = self.browse(cr, uid, data_ids[0]).model_id.model
        return model_name

    def get_color_name(self, cr, uid, key, context=None):
        res = {}
        reminder_id = self.search(cr, uid, [('name','=', key)])
        if reminder_id:
            color_name = self.browse(cr, uid, reminder_id[0]).color
            res.update({str(key): color_name})
        return res

    def get_unique_id(self, cr, uid, context=None):
        res = {}
        reminder_ids = self.search(cr, uid, [], context=context)
        for data in self.browse(cr, uid, reminder_ids, context=context):
            unique_id = 'ui' + str(data.id) + str(data.model_id.id) + str(data.field_id.id)
            res.update({str(data.name): unique_id})
        return res

    def set_record_header(self, cr, uid, context=None):
        reminder_ids = self.search(cr, uid, [], context=context)
        res = {}
        for data in self.browse(cr, uid, reminder_ids, context=context):
            field_res = {}
            field_label = []
            for display_data in data.popup_field_ids:
                field_res.update({str(display_data.name):str(display_data.field_description)})
            field_label.append(field_res)
            res.update({str(data.name): field_label})
        return res

    def set_notification(self, cr, uid, count=False, context=None):
        res = {}
        reminder_ids = self.search(cr, uid, [], context=context)
        today_date = datetime.date.today()
        cur_month_first_date = today_date + relativedelta(day=1)
        cur_month_last_date = today_date + relativedelta(day=1, months= +1, days= -1)
        next_month_first_date = today_date + relativedelta(day=1, months= +1)
        next_month_last_date = today_date + relativedelta(day=1, months= +2, days= -1)
        next_month = datetime.date.today() + relativedelta(months=1)
        maintenance_obj = self.pool.get('property.maintenance')
        maintenance_list = []
        
        if uid != SUPERUSER_ID:
            for partner in self.pool.get('res.users').browse(cr, uid, uid, context=context):
                agent_partner_id = partner.partner_id.id
                maintenanace_id = maintenance_obj.search(cr, uid, [('assign_to','=',agent_partner_id)], context=context)
        else:
            maintenanace_id = maintenance_obj.search(cr, uid, [], context=context)
        
        for data in self.browse(cr, uid, reminder_ids, context=context):
            today_date = datetime.date.today()
            data_ids = []
            rec_ids = []
            model_obj = self.pool.get(data.model_id.model)
            
            if data.search_option == 'current_month':
                if data.from_today:
                    if data.field_id.ttype in ['datetime']:
                        try:
                            cur_month_last_date = datetime.datetime.strptime(str(cur_month_last_date), DEFAULT_SERVER_DATETIME_FORMAT).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                        except:
                            cur_month_last_date = datetime.datetime.strptime(str(cur_month_last_date), '%Y-%m-%d').strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                        today_date = today_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                    if data.model_id.model != 'property.maintenance':
                        rec_ids = model_obj.search(cr, uid, [(data.field_id.name, '>=', today_date),
                                                             (data.field_id.name, '<=', cur_month_last_date)])
                    if data.model_id.model == 'property.maintenance' and data.field_id.name == 'last_record_update':
                        rec_ids = model_obj.search(cr, uid, [(data.field_id.name, '>=', today_date),
                                                             (data.field_id.name, '<=', cur_month_last_date)])
                        common_ids = set(maintenanace_id) & set(rec_ids)
                        data_ids = list(common_ids)

                else:
                    if data.field_id.ttype in ['datetime']:
                        try:
                            cur_month_last_date = datetime.datetime.strptime(str(cur_month_last_date),'%Y-%m-%d %H:%M:%S').strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                        except:
                            cur_month_last_date = datetime.datetime.strptime(str(cur_month_last_date),'%Y-%m-%d').strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                        try:
                            cur_month_first_date = datetime.datetime.strptime(str(cur_month_first_date),'%Y-%m-%d %H:%M:%S').strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                        except:
                            cur_month_first_date = datetime.datetime.strptime(str(cur_month_first_date),'%Y-%m-%d').strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                    if data.model_id.model != 'property.maintenance':
                        rec_ids = model_obj.search(cr, uid, [(data.field_id.name, '>=', today_date),
                                                             (data.field_id.name, '<=', cur_month_last_date)])
                    if data.model_id.model == 'property.maintenance' and data.field_id.name == 'last_record_update':
                        rec_ids = model_obj.search(cr, uid, [(data.field_id.name, '>=', today_date),
                                                             (data.field_id.name, '<=', cur_month_last_date)])
                        common_ids = set(maintenanace_id) & set(rec_ids)
                        data_ids = list(common_ids)
                        
            if data.search_option == 'next_month':
                if data.field_id.ttype in ['datetime']:
                    next_month_first_date = next_month_first_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                    next_month_last_date = next_month_last_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                if data.model_id.model != 'property.maintenance':
                        rec_ids = model_obj.search(cr, uid, [(data.field_id.name, '>=', today_date),
                                                             (data.field_id.name, '<=', cur_month_last_date)])
                if data.model_id.model == 'property.maintenance' and data.field_id.name == 'last_record_update':
                        rec_ids = model_obj.search(cr, uid, [(data.field_id.name, '>=', today_date),
                                                             (data.field_id.name, '<=', cur_month_last_date)])
                        common_ids = set(maintenanace_id) & set(rec_ids)
                        data_ids = list(common_ids)
                        
            if data.search_option == 'days':
                next_date = False
                if data.field_id.ttype in ['datetime']:
                    today_date = today_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                    next_date = datetime.date.today()+datetime.timedelta(days=data.duration_in_days)
                    next_date = next_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                if not next_date:
                    next_date = datetime.date.today()+datetime.timedelta(days=data.duration_in_days)
                    next_date = next_date.strftime(DEFAULT_SERVER_DATE_FORMAT)
                if data.model_id.model != 'property.maintenance':
                        rec_ids = model_obj.search(cr, uid, [(data.field_id.name, '>=', today_date),
                                                             (data.field_id.name, '<=', cur_month_last_date)])
                if data.model_id.model == 'property.maintenance' and data.field_id.name == 'last_record_update':
                        rec_ids = model_obj.search(cr, uid, [(data.field_id.name, '>=', today_date),
                                                             (data.field_id.name, '<=', cur_month_last_date)])
                        common_ids = set(maintenanace_id) & set(rec_ids)
                        data_ids = list(common_ids)
                        
                        
            if data.search_option == 'today':
                if data.field_id.ttype in ['datetime']:
                    today_date = today_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                if data.model_id.model != 'property.maintenance':
                        rec_ids = model_obj.search(cr, uid, [(data.field_id.name, '>=', today_date),
                                                             (data.field_id.name, '<=', cur_month_last_date)])
                if data.model_id.model == 'property.maintenance' and data.field_id.name == 'last_record_update':
                        rec_ids = model_obj.search(cr, uid, [(data.field_id.name, '>=', today_date),
                                                             (data.field_id.name, '<=', cur_month_last_date)])
                        common_ids = set(maintenanace_id) & set(rec_ids)
                        data_ids = list(common_ids)
                        
            read_data = []
            field_label = []
            field_res = {}
            for display_data in data.popup_field_ids:
                read_data.append(str(display_data.name))
                field_res.update({str(display_data.name):str(display_data.field_description)})
            field_label.append(field_res)
            model_data = model_obj.read(cr, uid, data_ids, read_data, context=context)
            for model in model_data:
                field_label.append(model)
            res.update({str(data.name): model_data})
        if count:
            total = 0
            for k,v in res.iteritems():
                total += len(v)
            return total
        return res

    name = fields.Char('Name', size=128)
    model_id = fields.Many2one('ir.model', 'Model', required=True)
    field_id = fields.Many2one('ir.model.fields', 'Fields', domain="[('model_id', '=', model_id),('ttype','in',['date','datetime'])]")
    popup_field_ids = fields.Many2many('ir.model.fields', 'popup_ir_model_field', 'field_id', 'popup_field_id', 'Display Fields', domain="[('model_id', '=', model_id)]")
    search_option = fields.Selection([('days', 'Days'), ('today', 'Today'), ('current_month', 'Current Month'), ('next_month', 'Next Month')], 'Search Option')
    duration_in_days = fields.Integer('Days')
    color = fields.Char('Color', size=64)
    from_today = fields.Boolean('From Today')
