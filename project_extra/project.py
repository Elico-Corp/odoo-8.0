# -*- coding: utf-8 -*-
# © 2015 Elico corp (www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, osv


class task(osv.osv):
    _inherit = "project.task"
    _name = "project.task"

    def _get_partner_prefix(self, partner_id):
        if partner_id:
            if partner_id.ref:
                prefix = '[' + partner_id.ref + ']'
            else:
                prefix = '[' + partner_id.name[0:3] + ']'
        else:
            prefix = ''
        return prefix

    def _callback_prefix_name(
            self, cr, uid, ids, field_name, arg, context=None):
        res = {}

        for task_id in self.browse(cr, uid, ids, context=context):
            if task_id:
                partner_id = task_id and task_id.project_id and \
                    task_id.project_id.partner_id
                prefix = self._get_partner_prefix(partner_id)

                if task_id.code_gap:
                    prefix += " " + task_id.code_gap + " - "

                res.update({
                    task_id.id: prefix + task_id.name
                })
        return res

    def _callback_prefix(self, cr, uid, ids, field_name, arg, context=None):
        res = {}

        for task_id in self.browse(cr, uid, ids, context=context):
            if task_id:
                partner_id = task_id and task_id.project_id and \
                    task_id.project_id.partner_id
                prefix = self._get_partner_prefix(partner_id)

                if task_id.code_gap:
                    prefix += " " + task_id.code_gap + " - "

                res.update({
                    task_id.id: prefix
                })
        return res

    def onchange_project(self, cr, uid, ids, project_id):
        res = super(task, self).onchange_project(cr, uid, ids, project_id)

        if project_id and 'value' in res:
            project = self.pool.get('project.project').browse(
                cr, uid, [project_id])
            # LY if no phase in project, leave phase empty
            res['value'].update(
                {
                    'phase_id': project[0] and
                    project[0].phase_ids and
                    project[0].phase_ids[0].id or False
                }
            )
        return res

    def _task_to_update_after_project_change(
            self, cr, uid, ids, fields=None, arg=None, context=None):
        if not isinstance(ids, list):
            ids = [ids]
        return self.pool.get('project.task').search(
            cr, uid, [('project_id', 'in', ids)]) or []

    _store_prefix_name = {
        'project.task': (lambda self, cr, uid, ids, context: ids,
                         ['code_gap', 'name'], 10),
        'project.project': (_task_to_update_after_project_change,
                            ['partner_id'], 10),
    }

    _columns = {
        'prefix_name': fields.function(
            _callback_prefix_name,
            store=_store_prefix_name,
            string='Task Name with Prefix',
            type='char',
            help="This field is computed automatically with name and project."
        ),
        'prefix': fields.function(
            _callback_prefix,
            string='Task Name Prefix',
            type='char',
            help="Prefix for task name"
        ),
    }
    _defaults = {
        'planned_hours': 4,
    }

    # LY: inherit open action, move the task to first stage
    def do_open(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = super(task, self).do_open(cr, uid, ids, context)
        vals = {}
        task_id = len(ids) and ids[0] or False
        task_id = self.browse(cr, uid, task_id, context=context)

        vals['type_id'] = task_id.project_id and \
            task_id.project_id.type_ids and \
            task_id.project_id.type_ids[0].id
        self.write(cr, uid, [task_id.id], vals, context=context)

        return res

    # LY: inherit close action, move the task to last stage
    def action_close(self, cr, uid, ids, context=None):
        res = super(task, self).action_close(cr, uid, ids, context)
        vals = {}
        task_id = len(ids) and ids[0] or False
        task_id = self.browse(cr, uid, task_id, context=context)

        # vals['type_id']= task_id.project_id and \
        # task_id.project_id.type_ids and \
        # task_id.project_id.type_ids[-1].id
        self.write(cr, uid, [task_id.id], vals, context=context)

        # # LY send a email reminder to task responsible and Eric.
        # mail_message = self.pool.get('mail.message')
        # subject = '[' + str(task_id.id) + '] "' + \
        #           task_id.name + '" is finished'
        # rendered_body = "Task [%d] \"%s\" is Finished.\n\n " \
        #                 "Task Descriptions:\n %s \n\n " \
        #                 "Project: \"%s\".\n " \
        #                 "Progress: %%%.2f. \n\n-----\n Good Job." \
        #                 " \n Project Task Reminder" % (
        #                     task_id.id,
        #                     task_id.name,
        #                     task_id.description,
        #                     task_id.project_id.name,
        #                     task_id.project_id.progress_rate or 100
        #                 )
        #
        # email_from = "admin@example.com"
        # email_to = [task_id.user_id.user_email]
        #
        # if task_id.user_id.user_email:
        #     email_cc = ["admin@example.com"]
        #
        # mail_message.schedule_with_attach(
        #     cr, uid, email_from, email_to, subject, rendered_body,
        #     model="project.task", email_cc=email_cc, email_bcc=None,
        #     reply_to=False, attachments=None, references=False,
        #     res_id=task_id.id, subtype='plain', context=context
        # )
        return res

    # LY: inherit normal priority, change color to yellow
    def set_normal_priority(self, cr, uid, ids, *args):
        super(task, self).set_normal_priority(cr, uid, ids, args)
        self.write(cr, uid, ids, {'color': 0}, context=None)
        return True

    # LY: inherit close action, move the task to last stage
    def set_high_priority(self, cr, uid, ids, *args):
        super(task, self).set_high_priority(cr, uid, ids, args)
        self.write(cr, uid, ids, {'color': 3}, context=None)
        return True


task()
