# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID

class ProjectProject(models.Model):
    _inherit = 'project.project'

    user_ids = fields.Many2many("res.users","rel_user_ids","rel_project_ids","user_project_rel",string="Users")
    
    @api.multi
    @api.onchange('project_team_ids')
    def onchange_team_ids(self):
        for rec in self:
            rec.user_ids = [(6, 0, [team.employee_id.user_id.id for team in rec.project_team_ids])]
            
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        if self.env.user.has_group('project.group_project_manager') and \
            not self.env.user.has_group('project_access_rights.group_project_admin') and \
            not self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                args += [('user_ids', 'in', self.env.user.id)]
                
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                args += [('user_ids', 'in', self.env.user.id)]
                
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                args += [('user_ids', 'in', self.env.user.id)]
        return super(ProjectProject, self).name_search(
            name=name, args=args, operator=operator, limit=limit,
        )
    
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = domain or []
        if self.env.user.has_group('project.group_project_manager') and \
            not self.env.user.has_group('project_access_rights.group_project_admin') and \
            not self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                domain.append(('user_ids', 'in', self.env.user.id))
                
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                domain.append(('user_ids', 'in', self.env.user.id))
                
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                domain.append(('user_ids', 'in', self.env.user.id))

        res = super(ProjectProject, self).search_read(domain=domain, fields=fields, offset=offset,
                                                      limit=limit, order=order)
        return res

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        domain = domain or []
        if self.env.user.has_group('project.group_project_manager') and \
            not self.env.user.has_group('project_access_rights.group_project_admin') and \
            not self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                domain.append(('user_ids', 'in', self.env.user.id))
        
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                domain.append(('user_ids', 'in', self.env.user.id))
                
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                domain.append(('user_ids', 'in', self.env.user.id))
        res = super(ProjectProject, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby,
                                                 lazy=lazy)
        return res

    @api.model
    def search(self, args, offset=0, limit=0, order=None, count=False):
        args = args or []
        if self.env.user.has_group('project.group_project_manager') and \
            not self.env.user.has_group('project_access_rights.group_project_admin') and \
            not self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                args.append(('user_ids', 'in', self.env.user.id))
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                args.append(('user_ids', 'in', self.env.user.id))
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                args.append(('user_ids', 'in', self.env.user.id))
        res = super(ProjectProject, self).search(args=args, offset=offset, limit=limit, order=order, count=count)
        return res
            
class ProjectTask(models.Model):
    _inherit = 'project.task'

    user_ids = fields.Many2many("res.users","rel_task_id","rel_user_id","user_task_rel",string="Users")
    
    @api.multi
    @api.onchange('employee_ids')
    def onchange_employee_ids(self):
        for rec in self:
            rec.user_ids = [(6, 0, [team.employee_id.user_id.id for team in rec.employee_ids])]
            
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        if self.env.user.has_group('project.group_project_manager') and \
            not self.env.user.has_group('project_access_rights.group_project_admin') and \
            not self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                args += [('user_ids', 'in', self.env.user.id)]
                
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                args += [('user_ids', 'in', self.env.user.id)]
                
#         if self.env.user.has_group('project.group_project_manager') and \
#             self.env.user.has_group('project_access_rights.group_project_admin') and \
#             self.env.user.has_group('project_access_rights.group_project_user') and \
#             self.env.user.has_group('project_access_rights.group_project_executive') and \
#             not self.env.user.has_group('project_access_rights.group_project_director'):
#                 args += [('user_ids', 'in', self.env.user.id)]
        return super(ProjectTask, self).name_search(
            name=name, args=args, operator=operator, limit=limit,
        )
    
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain = domain or []
        if self.env.user.has_group('project.group_project_manager') and \
            not self.env.user.has_group('project_access_rights.group_project_admin') and \
            not self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                domain.append(('user_ids', 'in', self.env.user.id))
                
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                domain.append(('user_ids', 'in', self.env.user.id))
                
#         if self.env.user.has_group('project.group_project_manager') and \
#             self.env.user.has_group('project_access_rights.group_project_admin') and \
#             self.env.user.has_group('project_access_rights.group_project_user') and \
#             self.env.user.has_group('project_access_rights.group_project_executive') and \
#             not self.env.user.has_group('project_access_rights.group_project_director'):
#                 domain.append(('user_ids', 'in', self.env.user.id))

        res = super(ProjectTask, self).search_read(domain=domain, fields=fields, offset=offset,
                                                      limit=limit, order=order)
        return res

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        domain = domain or []
        if self.env.user.has_group('project.group_project_manager') and \
            not self.env.user.has_group('project_access_rights.group_project_admin') and \
            not self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                domain.append(('user_ids', 'in', self.env.user.id))
        
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                domain.append(('user_ids', 'in', self.env.user.id))
                
#         if self.env.user.has_group('project.group_project_manager') and \
#             self.env.user.has_group('project_access_rights.group_project_admin') and \
#             self.env.user.has_group('project_access_rights.group_project_user') and \
#             self.env.user.has_group('project_access_rights.group_project_executive') and \
#             not self.env.user.has_group('project_access_rights.group_project_director'):
#                 domain.append(('user_ids', 'in', self.env.user.id))
        res = super(ProjectTask, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby,
                                                 lazy=lazy)
        return res

    @api.model
    def search(self, args, offset=0, limit=0, order=None, count=False):
        args = args or []
        if self.env.user.has_group('project.group_project_manager') and \
            not self.env.user.has_group('project_access_rights.group_project_admin') and \
            not self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                args.append(('user_ids', 'in', self.env.user.id))
        if self.env.user.has_group('project.group_project_manager') and \
            self.env.user.has_group('project_access_rights.group_project_admin') and \
            self.env.user.has_group('project_access_rights.group_project_user') and \
            not self.env.user.has_group('project_access_rights.group_project_executive') and \
            not self.env.user.has_group('project_access_rights.group_project_director'):
                args.append(('user_ids', 'in', self.env.user.id))
#         if self.env.user.has_group('project.group_project_manager') and \
#             self.env.user.has_group('project_access_rights.group_project_admin') and \
#             self.env.user.has_group('project_access_rights.group_project_user') and \
#             self.env.user.has_group('project_access_rights.group_project_executive') and \
#             not self.env.user.has_group('project_access_rights.group_project_director'):
#                 args.append(('user_ids', 'in', self.env.user.id))
        res = super(ProjectTask, self).search(args=args, offset=offset, limit=limit, order=order, count=count)
        return res