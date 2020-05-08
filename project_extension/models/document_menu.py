from odoo import api, fields, models
from datetime import date, datetime


class DocumentMenu(models.Model):
    _inherit = 'ir.attachment'
    _order = 'write_date'

    project_id = fields.Many2one('project.project', 'Project Name')
    task_id = fields.Many2one('project.task', 'Task', domain="[('project_id', '=', project_id)]")
    name = fields.Char('Attachment Name', required="1")
    description = fields.Text('Description')
    type_id = fields.Selection([('url', 'URL'), ('binary', 'FILE')], 'Type', required="1")
    datas = fields.Binary('Content')
    datas_fname = fields.Binary('File Name')
    url = fields.Text('URL')
    date_create = fields.Datetime(string="Date Created", default=datetime.now())
    owner = fields.Many2one('res.users', 'Owner', default=lambda self: self.env.user)

    @api.model
    def default_get(self, fields):
        res = super(DocumentMenu, self).default_get(fields)
        context = dict(self._context or {})
        if not 'active_model' in context or not 'active_id' in context:
            return res
        active_model = context.get('active_model')
        active_id = context.get('active_id')
        task = self.env['project.task'].browse(active_id)
        if active_model == 'project.task':
            res.update({'task_id': active_id, 'project_id': task.project_id.id})
        return res

    @api.model
    def create(self, vals):
        res = super(DocumentMenu, self).create(vals)
        if res.task_id:
            res.res_model = 'project.task'
            res.res_id = res.task_id.id
        return res
