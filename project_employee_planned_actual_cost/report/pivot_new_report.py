# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools, api
import logging
_logger = logging.getLogger(__name__)
from odoo import http
from odoo.http import request


class HrEmployee(models.Model):
    _inherit= "hr_timesheet_sheet.sheet"
  
    log_id1 = fields.Many2one('res.users', string='Current user', default=lambda self: self.env.user)
    group_viewer = fields.Many2one('res.groups', string='Project/Viewer', compute="_get_groups",store=True)
    group_user = fields.Many2one('res.groups', string='Project/User', compute="_get_groups",store=True)

    
    @api.depends('user_id')
    def _get_groups(self):
        for rec in self:
            if rec.user_id.has_group('project.group_project_manager'):
                rec.group_viewer = self.env.ref('project.group_project_manager')
           
            if rec.user_id.has_group('project_access_rights.group_project_user'):
                rec.group_user = self.env.ref('project_access_rights.group_project_user')
            
#     @api.one
#     def _get_current_login_user(self):
#         context = self._context
#         current_uid = context.get('uid')
#         self.log_id1 = self.env['res.users'].browse(current_uid)

class EmployeeTimeHistory(models.Model):
    _inherit = 'employee.time.history'
    
    leftover_val = fields.Float(sting="leftover_val",compute='_get_leftover_hours')
    related_leftover = fields.Float(sting="Related Leftover")
    spentover_val = fields.Float(sting="spentover",compute='_get_spentover_hours')
    related_spentover = fields.Float(sting="Related Spentover")
    related_rate = fields.Float(string="related_rate")
    rate_val = fields.Float(string="rate_val",compute='_get_rate')
      
    @api.depends('planned_hours','actual_hours')
    def _get_leftover_hours(self):
        for rec in self:
            rec.leftover_val = rec.leftover_hours
            rec.write({
                'related_leftover' : rec.leftover_hours,
                
            })

    @api.depends('planned_hours','actual_hours')
    def _get_spentover_hours(self):
        for rec in self:
            rec.spentover_val = rec.spentover_hours
            rec.write({
                'related_spentover' : rec.spentover_hours,
                
            })
              
    @api.depends('employee_id.timesheet_cost')
    def _get_rate(self):
        for rec in self:
            rec.rate_val = rec.employee_id.timesheet_cost
            rec.write({
                'related_rate' : rec.employee_id.timesheet_cost,
                
            })
              

    
   
class PivotReportNew(models.Model):
    _name = 'pivot.report.new'
    _description = "Project Employee Manhours"
    _auto = False
    _rec_name = "employee_id"
            
    employee_id = fields.Many2one('hr.employee', string="Employee", readonly=True)
    plan_hours = fields.Float(string="Plan Hours",readonly=True)
    actual_hours = fields.Float(string="Actual Hours",readonly=True)
    leftover_hours = fields.Float(string="Leftover Hours",readonly=True)
    spentover_hours = fields.Float(string="Spentover Hours",readonly=True)
    project_task = fields.Many2one('project.task',string='Project Task',readonly=True)
    project_id = fields.Many2one('project.project', string='Project', readonly=True) 
    user_id = fields.Many2one('res.users', string='Assigned To', readonly=True)
    
    def _get_project_team_executive_ids(self):
        emp_ids = []
        if self.env.user.has_group('project_access_rights.group_project_executive'):
            employee = self.env['hr.employee'].sudo().search([('user_id','=',self.env.user.id)])
            for line in self.env['project.team'].sudo().search([('employee_id','in',employee.ids)]):
                for l in line.project_details_id.project_team_ids:
                    emp_ids.append(l.employee_id.id)
        if self.env.user.has_group('project_access_rights.group_project_director') or self.env.user.has_group('project.group_project_manager'):
            employee = self.env['hr.employee'].search([])
            for line in employee:
                if line.id not in emp_ids:
                    emp_ids.append(line.id)

        return tuple(emp_ids)
    
    def _get_user_executive_project_ids(self):
        projects = tuple()
        p = []
        p1 = []
        if self.env.user.has_group('project_access_rights.group_project_executive'):
            employee = self.env['hr.employee'].sudo().search([('user_id','=',self.env.user.id)])
            for line in self.env['project.team'].sudo().search([('employee_id','in',employee.ids)]):
                if line.project_details_id and line.project_details_id.id not in projects:
                    p.append(line.project_details_id.id)
                    p1.append(line.project_details_id.id)
                    projects += (line.project_details_id.id,)
        if self.env.user.has_group('project_access_rights.group_project_director') or self.env.user.has_group('project.group_project_manager'):
            project = self.env['project.project'].search([])
            for line in project:
                if line.id not in projects:
                    p.append(line.id)
                    projects += (line.id,)
        
        if len(p) > 1:
            return projects
        if len(p) == 1:
            for i in p:
                p1.append(i)
            return tuple(p1)
    
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(PivotReportNew, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        self.init()
        return res
    
    def _select(self):
        select_str = """
            SELECT min(hts.id) as id,
                
                (CASE WHEN ((hts.group_viewer = %s or hts.group_user = %s) and (hts.user_id = %s)) 
                    or (%s = true) or (%s = true) or (%s = true and hr.id %s %s and pp.id %s %s)
                THEN hr.id
                ELSE null
                END) as employee_id, 
                            
                (CASE WHEN ((hts.group_viewer = %s or hts.group_user = %s) and (hts.user_id = %s)) 
                    or (%s = true) or (%s = true) or (%s = true and hr.id %s %s and pp.id %s %s)
                THEN pp.id
                ELSE null
                END) as project_id,
                
                (CASE WHEN ((hts.group_viewer = %s or hts.group_user = %s) and (hts.user_id = %s)) 
                    or (%s = true) or (%s = true) or (%s = true and hr.id %s %s and pp.id %s %s)  
                THEN pt.id
                ELSE null
                END) as project_task,
                
                (CASE WHEN ((hts.group_viewer = %s or hts.group_user = %s) and (hts.user_id = %s)) 
                    or (%s = true) or (%s = true) or (%s = true and hr.id %s %s and pp.id %s %s)
                THEN eth.planned_hours
                ELSE null
                END) as plan_hours,
                
                (CASE WHEN ((hts.group_viewer = %s or hts.group_user = %s) and (hts.user_id = %s)) 
                    or (%s = true) or (%s = true) or (%s = true and hr.id %s %s and pp.id %s %s)
                THEN eth.actual_hours
                ELSE null
                END) as actual_hours,
                
                (CASE WHEN ((hts.group_viewer = %s or hts.group_user = %s) and (hts.user_id = %s)) 
                    or (%s = true) or (%s = true) or (%s = true and hr.id %s %s and pp.id %s %s)
                THEN eth.related_leftover
                ELSE null
                END) as leftover_hours,
                
                (CASE WHEN ((hts.group_viewer = %s or hts.group_user = %s) and (hts.user_id = %s)) 
                    or (%s = true) or (%s = true) or (%s = true and hr.id %s %s and pp.id %s %s)
                THEN eth.related_spentover
                ELSE null
                END) as spentover_hours,
                
                (CASE WHEN ((hts.group_viewer = %s or hts.group_user = %s) and (hts.user_id = %s)) 
                    or (%s = true) or (%s = true) or (%s = true and hr.id %s %s and pp.id %s %s)
                THEN hts.user_id
                ELSE null
                END) as user_id
                
        """ % (self.env.ref('project.group_project_manager').id,self.env.ref('base.group_user').id,self.env.user.id,self.env.user.has_group('project_access_rights.group_project_admin'),self.env.user.has_group('project_access_rights.group_project_director'),self.env.user.has_group('project_access_rights.group_project_executive'),'in',self._get_project_team_executive_ids(),'in',self._get_user_executive_project_ids(),
               self.env.ref('project.group_project_manager').id,self.env.ref('base.group_user').id,self.env.user.id,self.env.user.has_group('project_access_rights.group_project_admin'),self.env.user.has_group('project_access_rights.group_project_director'),self.env.user.has_group('project_access_rights.group_project_executive'),'in',self._get_project_team_executive_ids(),'in',self._get_user_executive_project_ids(),
               self.env.ref('project.group_project_manager').id,self.env.ref('base.group_user').id,self.env.user.id,self.env.user.has_group('project_access_rights.group_project_admin'),self.env.user.has_group('project_access_rights.group_project_director'),self.env.user.has_group('project_access_rights.group_project_executive'),'in',self._get_project_team_executive_ids(),'in',self._get_user_executive_project_ids(),
               self.env.ref('project.group_project_manager').id,self.env.ref('base.group_user').id,self.env.user.id,self.env.user.has_group('project_access_rights.group_project_admin'),self.env.user.has_group('project_access_rights.group_project_director'),self.env.user.has_group('project_access_rights.group_project_executive'),'in',self._get_project_team_executive_ids(),'in',self._get_user_executive_project_ids(),
               self.env.ref('project.group_project_manager').id,self.env.ref('base.group_user').id,self.env.user.id,self.env.user.has_group('project_access_rights.group_project_admin'),self.env.user.has_group('project_access_rights.group_project_director'),self.env.user.has_group('project_access_rights.group_project_executive'),'in',self._get_project_team_executive_ids(),'in',self._get_user_executive_project_ids(),
               self.env.ref('project.group_project_manager').id,self.env.ref('base.group_user').id,self.env.user.id,self.env.user.has_group('project_access_rights.group_project_admin'),self.env.user.has_group('project_access_rights.group_project_director'),self.env.user.has_group('project_access_rights.group_project_executive'),'in',self._get_project_team_executive_ids(),'in',self._get_user_executive_project_ids(),
               self.env.ref('project.group_project_manager').id,self.env.ref('base.group_user').id,self.env.user.id,self.env.user.has_group('project_access_rights.group_project_admin'),self.env.user.has_group('project_access_rights.group_project_director'),self.env.user.has_group('project_access_rights.group_project_executive'),'in',self._get_project_team_executive_ids(),'in',self._get_user_executive_project_ids(),
               self.env.ref('project.group_project_manager').id,self.env.ref('base.group_user').id,self.env.user.id,self.env.user.has_group('project_access_rights.group_project_admin'),self.env.user.has_group('project_access_rights.group_project_director'),self.env.user.has_group('project_access_rights.group_project_executive'),'in',self._get_project_team_executive_ids(),'in',self._get_user_executive_project_ids(),
              )
        return select_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                hr.id,
                u.id,
                hts.id,
                pp.id,
                pt.id,
                eth.planned_hours,
                eth.actual_hours,
                eth.related_leftover,
                eth.related_spentover,
                hts.user_id,
                hts.group_viewer,
                hts.log_id1,
                hts.employee_id,
                aal.employee_id               
        """
        return group_by_str

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE view %s as
                %s
                FROM
                hr_timesheet_sheet_sheet hts 
                    left join hr_employee as hr on (hts.employee_id = hr.id)
                    left join res_users u on u.id = hts.user_id
                    left join account_analytic_line aal on (aal.sheet_id = hts.id)
                    left join project_project pp on (aal.project_id = pp.id)
                    left join project_task pt  on (pt.id = aal.task_id and pt.project_id = pp.id)
                    left join  employee_time_history eth on (eth.task_id = pt.id and eth.employee_id = hr.id)
               WHERE pt.active = 'true'
                %s
        """ % (self._table, self._select(), self._group_by()))
        
class ProjectEmployeeCostReport(models.Model):
    _name = 'project.employee.cost.report'
    _description = "Project Employee Cost"
    _auto = False
    
    employee_id = fields.Many2one('hr.employee', string="Employee", readonly=True)
    project_task = fields.Many2one('project.task', string='Project Task', readonly=True)
    project_id = fields.Many2one('project.project', string='Project', readonly=True) 
    plan_hours = fields.Float(string="Plan Hours", readonly=True)
    actual_hours = fields.Float(string="Actual Hours", readonly=True)
    leftover_hours = fields.Float(string="Leftover Hours", readonly=True)
    spentover_hours = fields.Float(string="Spentover Hours", readonly=True)
    cost = fields.Float(string='Cost', readonly=True)
    date = fields.Date(string="Date", readonly=True)
    spent_value = fields.Float(string="Spent Value", readonly=True)
    user_id = fields.Many2one('res.users', string='Assigned To', readonly=True)
    
    def _get_project_team_executive_ids(self):
        emp_ids = []
        if self.env.user.has_group('project_access_rights.group_project_executive'):
            employee = self.env['hr.employee'].search([('user_id','=',self.env.user.id)])
            for line in self.env['project.team'].search([('employee_id','in',employee.ids)]):
                for l in line.project_details_id.project_team_ids:
                    emp_ids.append(l.employee_id.id)
        if self.env.user.has_group('project_access_rights.group_project_director') or self.env.user.has_group('project.group_project_manager'):
            employee = self.env['hr.employee'].search([])
            for line in employee:
                if line.id not in emp_ids:
                    emp_ids.append(line.id)

        return tuple(emp_ids)
    
    def _get_user_executive_project_ids(self):
        projects = tuple()
        p = []
        p1 = []
        if self.env.user.has_group('project_access_rights.group_project_executive'):
            employee = self.env['hr.employee'].search([('user_id','=',self.env.user.id)])
            for line in self.env['project.team'].search([('employee_id','in',employee.ids)]):
                if line.project_details_id and line.project_details_id.id not in projects:
                    p.append(line.project_details_id.id)
                    p1.append(line.project_details_id.id)
                    projects += (line.project_details_id.id,)
        if self.env.user.has_group('project_access_rights.group_project_director') or self.env.user.has_group('project.group_project_manager'):
            project = self.env['project.project'].search([])
            for line in project:
                if line.id not in projects:
                    p.append(line.id)
                    projects += (line.id,)
        
        if len(p) > 1:
            return projects
        if len(p) == 1:
            for i in p:
                p1.append(i)
            return tuple(p1)
        
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ProjectEmployeeCostReport, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        self.init()
        return res
    
    def _select(self):
        select_str = """
            SELECT min(hts.id) as id,
                (CASE WHEN ((hts.group_viewer = %s or hts.group_user = %s) and (hts.user_id = %s)) 
                    or (%s = true) or (%s = true) or (%s = true and hr.id %s %s and pp.id %s %s)
                THEN hr.id
                ELSE null
                END) as employee_id, 
                            
                (CASE WHEN ((hts.group_viewer = %s or hts.group_user = %s) and (hts.user_id = %s)) 
                    or (%s = true) or (%s = true) or (%s = true and hr.id %s %s and pp.id %s %s)
                THEN pp.id
                ELSE null
                END) as project_id,
                
                (CASE WHEN ((hts.group_viewer = %s or hts.group_user = %s) and (hts.user_id = %s)) 
                    or (%s = true) or (%s = true) or (%s = true and hr.id %s %s and pp.id %s %s)  
                THEN pt.id
                ELSE null
                END) as project_task,
                
                (CASE WHEN ((hts.group_viewer = %s or hts.group_user = %s) and (hts.user_id = %s)) 
                    or (%s = true) or (%s = true) or (%s = true and hr.id %s %s and pp.id %s %s)
                THEN eth.planned_hours
                ELSE null
                END) as plan_hours,
                
                (CASE WHEN ((hts.group_viewer = %s or hts.group_user = %s) and (hts.user_id = %s)) 
                    or (%s = true) or (%s = true) or (%s = true and hr.id %s %s and pp.id %s %s)
                THEN eth.actual_hours
                ELSE null
                END) as actual_hours,
                
                (CASE WHEN ((hts.group_viewer = %s or hts.group_user = %s) and (hts.user_id = %s)) 
                    or (%s = true) or (%s = true) or (%s = true and hr.id %s %s and pp.id %s %s)
                THEN eth.related_leftover
                ELSE null
                END) as leftover_hours,
                
                (CASE WHEN ((hts.group_viewer = %s or hts.group_user = %s) and (hts.user_id = %s)) 
                    or (%s = true) or (%s = true) or (%s = true and hr.id %s %s and pp.id %s %s)
                THEN eth.related_spentover
                ELSE null
                END) as spentover_hours,
                
                (CASE WHEN ((hts.group_viewer = %s or hts.group_user = %s) and (hts.user_id = %s)) 
                    or (%s = true) or (%s = true) or (%s = true and hr.id %s %s and pp.id %s %s)
                THEN hts.user_id
                ELSE null
                END) as user_id,
                
                (CASE WHEN ((hts.group_viewer = %s or hts.group_user = %s) and (hts.user_id = %s)) 
                    or (%s = true) or (%s = true) or (%s = true and hr.id %s %s and pp.id %s %s)
                THEN aal.date
                ELSE null::date
                END) as date,
                
                (CASE WHEN ((hts.group_viewer = %s or hts.group_user = %s) and (hts.user_id = %s)) 
                    or (%s = true) or (%s = true) or (%s = true and hr.id %s %s and pp.id %s %s)
                THEN eth.related_rate
                ELSE null
                END) as cost,
                
                (CASE WHEN ((hts.group_viewer = %s or hts.group_user = %s) and (hts.user_id = %s)) 
                    or (%s = true) or (%s = true) or (%s = true and hr.id %s %s and pp.id %s %s)   
                THEN eth.actual_hours * eth.related_rate
                ELSE null
                END) as spent_value
                                
        """ % (self.env.ref('project.group_project_manager').id,self.env.ref('base.group_user').id,self.env.user.id,self.env.user.has_group('project_access_rights.group_project_admin'),self.env.user.has_group('project_access_rights.group_project_director'),self.env.user.has_group('project_access_rights.group_project_executive'),'in',self._get_project_team_executive_ids(),'in',self._get_user_executive_project_ids(),
               self.env.ref('project.group_project_manager').id,self.env.ref('base.group_user').id,self.env.user.id,self.env.user.has_group('project_access_rights.group_project_admin'),self.env.user.has_group('project_access_rights.group_project_director'),self.env.user.has_group('project_access_rights.group_project_executive'),'in',self._get_project_team_executive_ids(),'in',self._get_user_executive_project_ids(),
               self.env.ref('project.group_project_manager').id,self.env.ref('base.group_user').id,self.env.user.id,self.env.user.has_group('project_access_rights.group_project_admin'),self.env.user.has_group('project_access_rights.group_project_director'),self.env.user.has_group('project_access_rights.group_project_executive'),'in',self._get_project_team_executive_ids(),'in',self._get_user_executive_project_ids(),
               self.env.ref('project.group_project_manager').id,self.env.ref('base.group_user').id,self.env.user.id,self.env.user.has_group('project_access_rights.group_project_admin'),self.env.user.has_group('project_access_rights.group_project_director'),self.env.user.has_group('project_access_rights.group_project_executive'),'in',self._get_project_team_executive_ids(),'in',self._get_user_executive_project_ids(),
               self.env.ref('project.group_project_manager').id,self.env.ref('base.group_user').id,self.env.user.id,self.env.user.has_group('project_access_rights.group_project_admin'),self.env.user.has_group('project_access_rights.group_project_director'),self.env.user.has_group('project_access_rights.group_project_executive'),'in',self._get_project_team_executive_ids(),'in',self._get_user_executive_project_ids(),
               self.env.ref('project.group_project_manager').id,self.env.ref('base.group_user').id,self.env.user.id,self.env.user.has_group('project_access_rights.group_project_admin'),self.env.user.has_group('project_access_rights.group_project_director'),self.env.user.has_group('project_access_rights.group_project_executive'),'in',self._get_project_team_executive_ids(),'in',self._get_user_executive_project_ids(),
               self.env.ref('project.group_project_manager').id,self.env.ref('base.group_user').id,self.env.user.id,self.env.user.has_group('project_access_rights.group_project_admin'),self.env.user.has_group('project_access_rights.group_project_director'),self.env.user.has_group('project_access_rights.group_project_executive'),'in',self._get_project_team_executive_ids(),'in',self._get_user_executive_project_ids(),
               self.env.ref('project.group_project_manager').id,self.env.ref('base.group_user').id,self.env.user.id,self.env.user.has_group('project_access_rights.group_project_admin'),self.env.user.has_group('project_access_rights.group_project_director'),self.env.user.has_group('project_access_rights.group_project_executive'),'in',self._get_project_team_executive_ids(),'in',self._get_user_executive_project_ids(),
               self.env.ref('project.group_project_manager').id,self.env.ref('base.group_user').id,self.env.user.id,self.env.user.has_group('project_access_rights.group_project_admin'),self.env.user.has_group('project_access_rights.group_project_director'),self.env.user.has_group('project_access_rights.group_project_executive'),'in',self._get_project_team_executive_ids(),'in',self._get_user_executive_project_ids(),
               self.env.ref('project.group_project_manager').id,self.env.ref('base.group_user').id,self.env.user.id,self.env.user.has_group('project_access_rights.group_project_admin'),self.env.user.has_group('project_access_rights.group_project_director'),self.env.user.has_group('project_access_rights.group_project_executive'),'in',self._get_project_team_executive_ids(),'in',self._get_user_executive_project_ids(),
               self.env.ref('project.group_project_manager').id,self.env.ref('base.group_user').id,self.env.user.id,self.env.user.has_group('project_access_rights.group_project_admin'),self.env.user.has_group('project_access_rights.group_project_director'),self.env.user.has_group('project_access_rights.group_project_executive'),'in',self._get_project_team_executive_ids(),'in',self._get_user_executive_project_ids(),
              )
        return select_str

    def _group_by(self):
        group_by_str = """
            GROUP BY
                hr.id,
                u.id,
                hts.id,
                pp.id,
                pt.id,
                eth.planned_hours,
                eth.actual_hours,
                eth.related_leftover,
                eth.related_spentover,
                hts.user_id,
                hts.group_viewer,
                hts.log_id1,
                hts.employee_id,
                aal.employee_id,
                aal.date,
                eth.related_rate
             
        """
        return group_by_str

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE view %s as
                %s
                FROM
                
                hr_timesheet_sheet_sheet hts 
                    left join hr_employee as hr on (hts.employee_id = hr.id)
                    left join res_users u on u.id = hts.user_id
                    left join account_analytic_line aal on (aal.sheet_id = hts.id)
                    left join project_project pp on (aal.project_id = pp.id)
                    left join project_task pt  on (pt.id = aal.task_id and pt.project_id = pp.id)
                    left join  employee_time_history eth on (eth.task_id = pt.id and eth.employee_id = hr.id)
               WHERE pt.active = 'true'
                %s
        """ % (self._table, self._select(), self._group_by()))
        
# (CASE WHEN ((select count(*) from employee_time_history where (task_id = pt.id and employee_id = hr.id)) > 0)
#                     THEN  eth.related_rate/(select count(*) from employee_time_history where task_id = pt.id and employee_id = hr.id)
#                     ELSE eth.related_rate
#                     END) as cost,