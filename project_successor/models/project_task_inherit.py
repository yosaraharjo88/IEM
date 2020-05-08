from odoo import models, fields, api, _
from odoo.exceptions import Warning
from datetime import datetime, date
from datetime import timedelta


class confirm_wizard(models.TransientModel):
    _name = 'task.confirm_wizard'

    # warning_msg = fields.Text(default='The current date is not match with predecessor date and the lag days,are you still want to start the task?')
    result = fields.Html()
    @api.model
    def default_get(self,fields):
        res=super(confirm_wizard,self).default_get(fields)
        if self._context.get('active_id'):
            current_tast_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            project_task_id = self.env['project.task'].browse(self._context.get('active_id'))

            result ="""
            <h2>The current date is not match with predecessor date and the lag days,<br/>
            check below and more </h2>
            <h2>current date: """+str(current_tast_date)+"""</h2>
            <table width="100%" cellspacing="1" cellpadding="4" border="1" height="73">
                        <tbody>
                            <tr style="font-weight:bold;">
                                <th>&nbsp;Task&nbsp;</th>
                                <th>&nbsp;Actualdate&nbsp;&nbsp;  +</th>
                                <th>&nbsp;lag &nbsp;&nbsp; = </th>
                                <th>&nbsp;Final actual date &nbsp;</th>
                            </tr>
                        """

            count = 0
            
            for val in project_task_id.predecessor_ids:
                
                if val.parent_task_id.actual_start_date:
                    
                    if count <= 5:
                        count += 1
                        current_tast_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        parent_date_1 = datetime.strptime(val.parent_task_id.actual_start_date, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
                        parent_date_2 = datetime.strptime(parent_date_1, "%Y-%m-%d %H:%M:%S")
                        
                        lag_days = val.lag_qty
                        final_days = parent_date_2
                        if val.lag_type == 'day':
                            final_days = parent_date_2 + timedelta(days=lag_days)
                        if val.lag_type == 'hour':
                            final_days = parent_date_2 + timedelta(hours=lag_days)
                        if val.lag_type == 'minute':
                            final_days = parent_date_2 + timedelta(minutes=lag_days)
                        f_days = final_days.strftime('%Y-%m-%d %H:%M:%S')
                        if f_days > current_tast_date:

                            result += (""" <tr>
                                            <td>&nbsp;%s&nbsp;</td>
                                            <td>&nbsp;%s&nbsp;</td>
                                            <td>&nbsp;%s(%s)&nbsp;</td>
                                            <td>&nbsp;%s&nbsp;</td>
                                           </tr>
                                        """) % (val.parent_task_id.name, parent_date_2,lag_days,val.lag_type,f_days)
            result += """</tbody>
                                            </table><br/>
                        <h2>Are you still want to start the task?</h2>"""
        res.update({'result':result})
        return res




    @api.multi
    def yes_confirm(self):
        if self._context.get('active_id'):
            project_task_id = self.env['project.task'].browse(self._context.get('active_id'))
            project_task_id.state = 'in_progress'

    @api.multi
    def no(self):
        return False


class ProjectTask(models.Model):
    _inherit = 'project.task'

    successor_ids = fields.One2many('project.task.successor', 'task_id')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ], string='Status', default="draft", track_visibility='onchange')


    def action_progress(self):
        self.actual_start_date = datetime.now()
        self.project_id.actual_start_date = datetime.now()

        flag1 = True
        flag2 = True
        
        if self.predecessor_ids:
            for val in self.predecessor_ids:
                if val.type == 'FS':
                    if val.parent_task_id.state == 'completed':
                        flag1 = True
                    else:
                        flag1 = False
                        raise Warning(_("Before start your predecessor %s task status must be finished")% val.parent_task_id.name)
                if val.type == 'SS':
                    if val.parent_task_id.state == 'in_progress':
                        flag2 = True
                    else:
                        raise Warning(_("Before start your predecessor %s task status must be inprogress")% val.parent_task_id.name)
                        flag2 = False

            for val in self.predecessor_ids:
                if val.parent_task_id.actual_start_date:
                        current_tast_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        parent_date_1 = datetime.strptime(val.parent_task_id.actual_start_date, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
                        parent_date_2 = datetime.strptime(parent_date_1, "%Y-%m-%d %H:%M:%S")
                        
                        lag_days = val.lag_qty
                        final_days = parent_date_2
                        if val.lag_type == 'day':
                            final_days = parent_date_2 + timedelta(days=lag_days)
                        if val.lag_type == 'hour':
                            final_days = parent_date_2 + timedelta(hours=lag_days)
                        if val.lag_type == 'minute':
                            final_days = parent_date_2 + timedelta(minutes=lag_days)
                        f_days = final_days.strftime('%Y-%m-%d %H:%M:%S')
                        
                        if f_days > current_tast_date:
                                return {
                                'name': 'Are you sure?',
                                'type': 'ir.actions.act_window',
                                'res_model': 'task.confirm_wizard',
                                'view_mode': 'form',
                                'view_type': 'form',
                                'target': 'new',
                            }

           

        if flag1 == True and flag2 == True:
            if self.project_id.state_project == 'draft':
                self.project_id.write({'state_project': 'progress'})
            self.state ='in_progress'
            

    def action_completed(self):
        self.date_finished = datetime.now()
        self.project_id.actual_end_date = datetime.now()
        flag1 = True
        flag2 = True
        flag3 = True
        
        if self.predecessor_ids:
            for val in self.predecessor_ids:
                if val.type == 'FF':
                    if val.parent_task_id.state == 'completed':
                        flag1 = True
                    else:
                        flag1 = False
                        raise Warning(_("Before finish your task predecessor %s task status must be finished")% val.parent_task_id.name)
                if val.type == 'SF':
                    if val.parent_task_id.state == 'in_progress':
                        flag2 = True
                    else:
                        raise Warning(_("Before finish your task predecessor %s task status must be inprogress")% val.parent_task_id.name)
                        flag2 = False

        if flag1 == True and flag2 == True:
            self.state = 'completed'
        incomplete_tasks = self.env['project.task'].search([('project_id', '=', self.project_id.id), ('state', 'not in', ['completed', 'cancelled'])])
        if not incomplete_tasks:
            self.project_id.state_project = 'done'


class ProjectTaskPredecessor(models.Model):
    _inherit = 'project.task.predecessor'

    @api.model
    def _get_lag_type(self):
        value = [
            ('minute', _('minute')),
            ('hour', _('hour')),
            ('day', _('day')),
            # ('percent', _('percent')),
        ]
        return value

    @api.model
    def create(self, vals):
        new_id = super(ProjectTaskPredecessor, self).create(vals)
        if new_id.type == u'FS':
            new_id.parent_task_id.successor_ids = [(0, 0, {
                'parent_task_id': new_id.task_id.id,
                'lag_quantity': new_id.lag_qty,
                'type': u'SF',
            })]
        else:
            new_id.parent_task_id.successor_ids = [(0, 0, {
                'parent_task_id': new_id.task_id.id,
                'lag_quantity': new_id.lag_qty,
            })]
        return new_id

    @api.multi
    def write(self, vals):
        old = self.task_id
        result = super(ProjectTaskPredecessor, self).write(vals)
        if result:
            to_del = self.env['project.task.successor'].search([('parent_task_id', '=', old.id)])
            if to_del:
                to_del[0].unlink()
            if self.type == u'FS':
                self.parent_task_id.successor_ids = [(0, 0, {
                    'parent_task_id': self.task_id.id,
                    'lag_quantity': self.lag_qty if self.lag_qty else 0,
                    'type': u'SF',
                })]
            else:
                self.parent_task_id.successor_ids = [(0, 0, {
                    'parent_task_id': self.task_id.id,
                    'lag_quantity': self.lag_qty if self.lag_qty else 0,
                })]

        return result


class ProjectTaskSuccessor(models.Model):
    _name = 'project.task.successor'

    task_id = fields.Many2one('project.task')
    parent_task_id = fields.Many2one('project.task', 'Task', required=True, ondelete='restrict',
                                     domain="[('project_id','=', parent.project_id), ('id', '!=', parent.id)]")
    child_task = fields.Char('Child Task')

    @api.model
    def _get_link_type(self):
        value = [
            ('FS', _('Finish to Start (FS)')),
            ('SS', _('Start to Start (SS)')),
            ('FF', _('Finish to Finish (FF)')),
            ('SF', _('Start to Finish (SF)')),

        ]
        return value

    type = fields.Selection('_get_link_type',
                            string='Type',
                            required=True,
                            default='FS')
    lag_quantity = fields.Integer(string='Lag', default=0)

    @api.model
    def _get_lag_type(self):
        value = [
            ('minute', _('minute')),
            ('hour', _('hour')),
            ('day', _('day')),
            ('percent', _('percent')),
        ]
        return value

    lag_type = fields.Selection('_get_lag_type',
                                string='Lag type',
                                required=True,
                                default='day')
    related_task = fields.Char('Related Task')
