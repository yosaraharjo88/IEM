from odoo import api, fields, models, SUPERUSER_ID


class StageDetails(models.Model):
    _inherit = 'project.task'


    doc_count = fields.Integer(compute='_compute_attached_docs_count', string="Number of attached documents")
    sequence_id = fields.Char('Name')

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].get('project.task')
        vals['sequence_id'] = seq
        # context: no_log, because subtype already handle this
        context = dict(self.env.context, mail_create_nolog=True)

        # for default stage
        if vals.get('project_id') and not context.get('default_project_id'):
            context['default_project_id'] = vals.get('project_id')
        # user_id change: update date_assign
        if vals.get('user_id'):
            vals['date_assign'] = fields.Datetime.now()
        task = super(StageDetails, self.with_context(context)).create(vals)
        return task

    @api.multi
    # Method that computes the number of docs attached to each task:
    def _compute_attached_docs_count(self):
        Attachment = self.env['ir.attachment']
        for task in self:
            task.doc_count = Attachment.search_count([
                ('res_model', '=', 'project.task'), ('res_id', 'in', self.ids)])

    # Method that returns the task attachments view settings:
    def attachment_tree_view(self):
        self.ensure_one()
        domain = [('res_model', '=', 'project.task'), ('res_id', 'in', self.ids)]
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'help': _('''<p class="o_view_nocontent_smiling_face">
                           Documents are attached to the tasks and issues of your project.</p><p>
                           Send messages or log internal notes with attachments to link
                           documents to your project.
                       </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        }

