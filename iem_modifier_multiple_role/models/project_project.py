# -*- coding: utf-8 -*-
from odoo import fields, models, tools, api
import logging
_logger = logging.getLogger(__name__)
from odoo import http
from odoo.http import request

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    project_child_ids = fields.One2many("res.users.project.child" , 'project_parent_id' ,string="Project Child")
    
class ResUsers(models.Model):
    _name = 'res.users.project.child'
    
    project_parent_id = fields.Many2one('res.users', string='Project Parent')
    child_id = fields.Many2one("res.users" ,string="Project Child")
    
class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.model
    def check_action(self,record_id):
        if record_id:
            if self.env.user and self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                record = self.sudo().browse(record_id)
                if record.project_id:
                    team_ids = [team.employee_id.user_id.id for team in record.project_id.project_team_ids if team.role_id.name in ['PM','PD']]
                    if self.env.user.id in team_ids:
                        return True
                    else:
                        return False
                else:
                    return True
            else:
                return True
        else:
            return True

class ProjectProject(models.Model):
    _inherit = 'project.project'
    # _order = "project_number asc"

    pd_id = fields.Many2one('res.users',string='PD')
    
    @api.model
    def check_action(self,record_id):
        if record_id:
            if self.env.user and self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                record = self.sudo().browse(record_id)
                team_ids = [team.employee_id.user_id.id for team in record.project_team_ids if team.role_id.name in ['PM','PD']]
                if self.env.user.id in team_ids:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return True
    
    @api.multi
    @api.onchange('project_team_ids')
    def onchange_team_ids(self):
        for rec in self:
            rec.user_ids = [(6, 0, [team.employee_id.user_id.id for team in rec.project_team_ids])]
            for pteam in rec.project_team_ids:
                if pteam.role_id.name == 'PD':
                    for team in rec.project_team_ids:
                        if team.role_id.name in ['PM','User']:
                            child_id = self.env['res.users.project.child'].search([('project_parent_id','=',pteam.employee_id.user_id.id),('child_id','=',team.employee_id.user_id.id)])
                            if not child_id:
                                child_id = self.env['res.users.project.child'].create({'project_parent_id': pteam.employee_id.user_id.id,
                                                                                       'child_id': team.employee_id.user_id.id,})
                if pteam.role_id.name == 'PM':
                    for team in rec.project_team_ids:
                        if team.role_id.name in ['User']:
                            child_id = self.env['res.users.project.child'].search([('project_parent_id','=',pteam.employee_id.user_id.id),('child_id','=',team.employee_id.user_id.id)])
                            if not child_id:
                                child_id = self.env['res.users.project.child'].create({'project_parent_id': pteam.employee_id.user_id.id,
                                                                            'child_id': team.employee_id.user_id.id,})

class ProjectEmployeeCostListReport(models.Model):
    _name = 'project.employee.cost.list.report'
    _description = "Project Employee Cost"
    
    employee_id = fields.Many2one('hr.employee', string="Employee", readonly=True)
    project_task = fields.Many2one('project.task', string='Project Task', readonly=True)
    project_id = fields.Many2one('project.project', string='Project', readonly=True)
    pd_id = fields.Many2one('res.users',string='PD', readonly=True)
    plan_hours = fields.Float(string="Plan Hours", readonly=True)
    cost_spend_value = fields.Float(string="Plan Hours", compute='compute_cost_spent_value',store=True)
    actual_hours = fields.Float(string="Actual Hours", readonly=True)
    leftover_hours = fields.Float(string="Leftover Hours", readonly=True)
    spentover_hours = fields.Float(string="Spentover (%)", readonly=True)
    cost = fields.Float(string='Cost', readonly=True)
    date = fields.Date(string="Date", readonly=True)
    spent_value = fields.Float(string="Spent Value", readonly=True)
    user_id = fields.Many2one('res.users', string='Assigned To', readonly=True)

    @api.multi
    def compute_cost_spent_value(self):
        print"function called "
        pro_ids = self.search([])
        pro_ids = self.search([('project_task','=',505)])
        # print"pro_ids ",pro_ids
        for record in pro_ids:
            if record.project_task:
                print"task ",record.project_task.id,record.project_task.name
                total_cost = 0.00
                total_spent_value_cost = 0.00
                print"record.project_task.employee_ids ",record.project_task.employee_ids
                for task in record.project_task.employee_ids:
                    print"self.employee_id.id ",record.employee_id.id,record.employee_id.name
                    print"task.employee_id.id",task.employee_id.id,task.employee_id.name
                    if task.employee_id.id == record.employee_id.id:
                        total_cost =+ task.rate_val
                        mul_val = (task.actual_hours * task.rate_val)
                        total_spent_value_cost =+ mul_val
                        print"total_cost ",total_cost
                        print"spent_value_cost0",total_spent_value_cost

                record.cost = total_cost
                record.spent_value = total_spent_value_cost
                print"rec cost00",record.cost
                print"record.spent value",record.spent_value

            # 'cost': sum([x.rate_val for x in line.task_id.employee_ids if x.employee_id.id == self.employee_id.id]),
            # 'date': line.date,
            # 'spent_value': sum([x.actual_hours * x.rate_val for x in line.task_id.employee_ids if
            #                     x.employee_id.id == self.employee_id.id]),
    
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                args += [('user_id', 'in', [self.env.user.id]+[x.child_id.id for x in self.env.user.project_child_ids])]

        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                args += [('pd_id', '=', self.env.user.id)]
        return super(ProjectEmployeeCostListReport, self).name_search(
            name=name, args=args, operator=operator, limit=limit,
        )
    
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = domain or []
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                domain.append(('user_id', 'in', [self.env.user.id]+[x.child_id.id for x in self.env.user.project_child_ids]))
                
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                domain.append(('pd_id', '=', self.env.user.id))

        res = super(ProjectEmployeeCostListReport, self).search_read(domain=domain, fields=fields, offset=offset,
                                                      limit=limit, order=order)
        return res

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        domain = domain or []
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                domain.append(('user_id', 'in', [self.env.user.id]+[x.child_id.id for x in self.env.user.project_child_ids]))
        
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                domain.append(('pd_id', '=', self.env.user.id))
        res = super(ProjectEmployeeCostListReport, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby,
                                                 lazy=lazy)
        return res

    @api.model
    def search(self, args, offset=0, limit=0, order=None, count=False):
        args = args or []
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                args.append(('user_id', 'in', [self.env.user.id]+[x.child_id.id for x in self.env.user.project_child_ids]))
#         
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                args.append(('pd_id', '=', self.env.user.id))
        res = super(ProjectEmployeeCostListReport, self).search(args=args, offset=offset, limit=limit, order=order, count=count)
        return res
    
class ProjectEmployeeManhoursReport(models.Model):
    _name = 'project.employee.manhours.report'
    _description = "Project Employee Manhours"
    # _rec_name = "employee_id"

    employee_id = fields.Many2one('hr.employee', string="Employee", readonly=True)
    plan_hours = fields.Float(string="Plan Hours",readonly=True)
    actual_hours = fields.Float(string="Actual Hours",readonly=True)
    pd_id = fields.Many2one('res.users',string='PD', readonly=True)
    leftover_hours = fields.Float(string="Leftover Hours",readonly=True)
    spentover_hours = fields.Float(string="Spentover  (%)",readonly=True)
    project_task = fields.Many2one('project.task',string='Project Task',readonly=True)
    project_id = fields.Many2one('project.project', string='Project', readonly=True) 
    user_id = fields.Many2one('res.users', string='Assigned To', readonly=True)
    
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                args += [('user_id', 'in', [self.env.user.id]+[x.child_id.id for x in self.env.user.project_child_ids])]

        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                args += [('pd_id', '=', self.env.user.id)]
        return super(ProjectEmployeeManhoursReport, self).name_search(
            name=name, args=args, operator=operator, limit=limit,
        )
    
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = domain or []
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                domain.append(('user_id', 'in', [self.env.user.id]+[x.child_id.id for x in self.env.user.project_child_ids]))
                
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                domain.append(('pd_id', '=', self.env.user.id))

        res = super(ProjectEmployeeManhoursReport, self).search_read(domain=domain, fields=fields, offset=offset,
                                                      limit=limit, order=order)
        return res

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        domain = domain or []
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                domain.append(('user_id', 'in', [self.env.user.id]+[x.child_id.id for x in self.env.user.project_child_ids]))
        
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                domain.append(('pd_id', '=', self.env.user.id))
        res = super(ProjectEmployeeManhoursReport, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby,
                                                 lazy=lazy)
        return res

    @api.model
    def search(self, args, offset=0, limit=0, order=None, count=False):
        args = args or []
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                args.append(('user_id', 'in', [self.env.user.id]+[x.child_id.id for x in self.env.user.project_child_ids]))
#         
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                args.append(('pd_id', '=', self.env.user.id))
        res = super(ProjectEmployeeManhoursReport, self).search(args=args, offset=offset, limit=limit, order=order, count=count)
        return res
    
class Timesheet(models.Model):
    _inherit = 'hr_timesheet_sheet.sheet'

    @api.multi
    def action_submit(self):
        res = super(Timesheet, self).action_submit()
        self.create_employee_cost()
        return res
       
    @api.multi
    def _create_cost_record(self, cost_vals):
        return self.env['project.employee.cost.list.report'].create(cost_vals)
    
    @api.multi
    def _create_manhours_record(self, manhours_vals):
        return self.env['project.employee.manhours.report'].create(manhours_vals)
       
    @api.multi
    def create_employee_cost(self):
        if self.timesheet_ids:
            for line in self.timesheet_ids:
                cost_ids = self.env['project.employee.cost.list.report'].search([('employee_id','=',self.employee_id.id),
                                                                                 ('project_id','=',line.project_id.id),
                                                                                 ('project_task','=',line.task_id.id)], limit=1)
                cost_vals = {'employee_id': self.employee_id.id,
                             'project_id': line.project_id.id,
                             'pd_id': line.project_id.pd_id.id,
                             'project_task': line.task_id.id,
                             'plan_hours': sum([x.planned_hours for x in line.task_id.employee_ids if x.employee_id.id == self.employee_id.id]),
                             'actual_hours': sum([x.actual_hours for x in line.task_id.employee_ids if x.employee_id.id == self.employee_id.id]),
                             'leftover_hours': sum([x.leftover_val for x in line.task_id.employee_ids if x.employee_id.id == self.employee_id.id]),
                             'spentover_hours': sum([x.spentover_val for x in line.task_id.employee_ids if x.employee_id.id == self.employee_id.id]),
                             'cost': sum([x.rate_val for x in line.task_id.employee_ids if x.employee_id.id == self.employee_id.id]),
                             'date': line.date,
                             'spent_value': sum([x.actual_hours * x.rate_val for x in line.task_id.employee_ids if x.employee_id.id == self.employee_id.id]),
                             'user_id': self.user_id.id,
                             }
                if not cost_ids:
                    self._create_cost_record(cost_vals)
                else:
                    cost_ids.write(cost_vals)
                manhours_ids = self.env['project.employee.manhours.report'].search([('employee_id','=',self.employee_id.id),
                                                                                 ('project_id','=',line.project_id.id),
                                                                                 ('project_task','=',line.task_id.id)], limit=1)

                project_team_ids = self.env['project.team'].search([('project_details_id', '=', line.project_id.id)])

                emp_list = []
                for team in project_team_ids:
                    emp_list.append(team.employee_id.id)
                print"emp_list  as emp_list  ",emp_list
                print"[(6, 0, [team.employee_id.user_id.id for team in rec.project_team_ids])]",[(6, 0, [team.employee_id.user_id.id for team in line.project_id.project_team_ids])]
                # 'employee_id': self.employee_id.id is changing toproject related project team tabs(employees)
                manhours_vals = {'employee_id': self.employee_id.id,
                                 'project_id': line.project_id.id,
                                 'project_task': line.task_id.id,
                                 'pd_id': line.project_id.pd_id.id,
                                 'plan_hours': sum([x.planned_hours for x in line.task_id.employee_ids if x.employee_id.id == self.employee_id.id]),
                                 'actual_hours': sum([x.actual_hours for x in line.task_id.employee_ids if x.employee_id.id == self.employee_id.id]),
                                 'leftover_hours': sum([x.leftover_val for x in line.task_id.employee_ids if x.employee_id.id == self.employee_id.id]),
                                 'spentover_hours': sum([x.spentover_val for x in line.task_id.employee_ids if x.employee_id.id == self.employee_id.id]),
                                 'user_id': self.user_id.id,
                                 }
                if not manhours_ids:
                    self._create_manhours_record(manhours_vals)
                else:
                    manhours_ids.write(manhours_vals)
