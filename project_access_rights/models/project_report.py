# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# from odoo import fields, models, tools, api
# 
# class ReportProjectTaskUser(models.Model):
#     _inherit = "report.project.task.user"
#     
#     def _select(self):
#         select_str = """
#              SELECT
#                     (select 1 ) AS nbr,
#                     t.id as id,
#                     t.date_start as date_start,
#                     t.date_end as date_end,
#                     t.date_last_stage_update as date_last_stage_update,
#                     t.date_deadline as date_deadline,
#                     abs((extract('epoch' from (t.write_date-t.date_start)))/(3600*24))  as no_of_days,
#                     t.user_id,
#                     t.project_id,
#                     t.priority,
#                     t.name as name,
#                     t.company_id,
#                     t.partner_id,
#                     t.stage_id as stage_id,
#                     t.kanban_state as state,
#                     (extract('epoch' from (NULLIF(t.date_end, t.write_date)-t.create_date)))/(3600*24)  as closing_days,
#                     (extract('epoch' from (t.date_start-t.create_date)))/(3600*24)  as opening_days,
#                     (extract('epoch' from (t.date_deadline-(now() at time zone 'UTC'))))/(3600*24)  as delay_endings_days
#         """
#         return select_str
#     
#     def _from(self):
#         from_str = """
#                 project_task t
#                       join project_project p on (t.project_id=p.id)
#                       join project_team pt on (pt.project_details_id=p.id)
#                       join employee_time_history et on (et.task_id=t.id)
#                       join hr_employee hp on (hp.id=pt.employee_id)
#                       join hr_employee ht on (ht.id=et.employee_id)
#                       join res_users rp on (rp.login=hp.work_email)
#                       join res_users rt on (rt.login=ht.work_email)
#         """
#         return from_str
# 
#     def _group_by(self):
#         group_by_str = """
#                 GROUP BY
#                     t.id,
#                     t.create_date,
#                     t.write_date,
#                     t.date_start,
#                     t.date_end,
#                     t.date_deadline,
#                     t.date_last_stage_update,
#                     t.user_id,
#                     t.project_id,
#                     t.priority,
#                     t.name,
#                     t.company_id,
#                     t.partner_id,
#                     t.stage_id
#         """
#         return group_by_str
#     
#     def _where(self):
#         where_str = """
#                 WHERE t.active = 'true' and
#                 rp.id = %s and
#                 rt.id = %s
#         """ % (self.env.user.id, self.env.user.id)
#         print "where_str..........................",self.env['project.project'].get_current_user()
#         return where_str
# 
#     def init(self):
#         tools.drop_view_if_exists(self._cr, self._table)
#         self._cr.execute("""
#             CREATE view %s as
#               %s
#               FROM (%s)
#                 %s
#                 %s
#         """ % (self._table, self._select(), self._from(), self._where(), self._group_by()))
