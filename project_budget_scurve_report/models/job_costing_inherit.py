import logging
from odoo import api, fields, models
from odoo.exceptions import ValidationError

from datetime import datetime
from datetime import timedelta

_logger = logging.getLogger(__name__)


# For Project vs Budget Table
class ProjectProjectInherit(models.Model):
    _inherit = 'project.project'

    # get each day actual budget
    @api.multi
    def get_actual_budget(self, task):
        job_cost_sheet_ids = self.env["job.costing"].search([('task_id', '=', task.id)])
        total_price = 0.0
        for job_cost_sheet in job_cost_sheet_ids:
            acc_inv_ids = self.env['account.invoice.line'].search([('job_cost_id', '=', job_cost_sheet.id)])
            for acc_inv in acc_inv_ids:
                total_price += acc_inv.price_subtotal
        total_task_duration = 0
        for task_id in task:
            task_start_date = datetime.strptime(task_id.start_date, '%Y-%m-%d %H:%M:%S').date()
            task_end_date = datetime.strptime(task_id.p_end_date, '%Y-%m-%d %H:%M:%S').date()
            task_duration = ((task_end_date - task_start_date) + timedelta(days=1)).days
            total_task_duration = total_task_duration + task_duration
        per_day_actual_budget = (total_price / total_task_duration)
        if total_price == 0.0:
            pday_actual_budget_percentage = (per_day_actual_budget / 1) * 100
        else:
            pday_actual_budget_percentage = (per_day_actual_budget / total_price) * 100
        # actual budget per day and per day in percentage
        actual_budget = {}
        actual_budget.update({"per_day_actual_budget": per_day_actual_budget,
                              "pday_actual_budget_percentage": pday_actual_budget_percentage})
        return actual_budget

    # Get each day budget amount
    @api.multi
    def get_each_day_budget(self, task):
        job_cost_sheet = self.env["job.costing"].search([('task_id', '=', task.id)])
        total_task_duration = 0
        for task in job_cost_sheet.task_id:
            task_start_date = datetime.strptime(task.start_date, '%Y-%m-%d %H:%M:%S').date()
            task_end_date = datetime.strptime(task.p_end_date, '%Y-%m-%d %H:%M:%S').date()
            task_duration = ((task_end_date - task_start_date) + timedelta(days=1)).days
            total_task_duration = total_task_duration + task_duration
        per_day_budget = (job_cost_sheet.jobcost_total / total_task_duration)
        return per_day_budget

    # Get each day budget amount percentage
    @api.multi
    def get_each_day_budget_per(self, per_day_budget):
        job_cost_sheets = self.env["job.costing"].search([('project_id', '=', self.id)])
        job_cost_total = 0
        for job_cost_sheet in job_cost_sheets:
            job_cost_total = job_cost_total + job_cost_sheet.jobcost_total
        each_day_budget_planned_per = ((per_day_budget / job_cost_total) * 100)
        return each_day_budget_planned_per

    def merge_progress_budget(self):
        # This is list of Project Budget data
        project_budget_datas = self.get_project_budget_data()

        # This is list of Project Progress data
        project_datas = self.gen_table()

        merge_list = []
        for rec_progress in project_datas:
            for rec_budget in project_budget_datas:
                if rec_progress['week'] == rec_budget['week']:
                    rec_progress.update(rec_budget)
                    merge_list.append(rec_progress)

        if len(merge_list):
            return merge_list
        else:
            raise ValidationError("Project start date and end date both not valid!")

    def get_project_budget_data(self):
        if not (self.project_start_date and self.project_end_date):
            raise ValidationError("Project Start Date and End Date not found!")
        else:
            project_start_date = datetime.strptime(self.project_start_date, '%Y-%m-%d %H:%M:%S').date()
            project_end_date = datetime.strptime(self.project_end_date, '%Y-%m-%d %H:%M:%S').date()

        job_cost_sheets = self.env["job.costing"].search([('project_id', '=', self.id)])
        get_last_date = []
        if not job_cost_sheets:
            raise ValidationError("Job Cost Sheets not found of this Project!")
        for job_cost_sheet in job_cost_sheets:
            for task in job_cost_sheet.task_id:
                for progress_history in task.task_progress_ids:
                    if not progress_history:
                        raise ValidationError("Progress History not found of '%s' task!" % task.name)
                    data = {'progress_history_id': progress_history.id,
                            'progress_end_date': progress_history.progress_end_date}
                    get_last_date.append(data)
        newlist = sorted(get_last_date, key=lambda k: k['progress_end_date'])
        last_date = newlist[-1].get("progress_end_date")
        last_date = datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S').date()
        # from progress history
        if project_end_date <= last_date:
            last_date_report = last_date
        # from project last date
        else:
            last_date_report = project_end_date

        week_start_date = project_start_date
        week_number = 0
        add7days = 0
        addtoenddate = 0
        total_planned_budget_each_week = 0
        total_actual_budget_each_week = 0
        total_per_week_budget_percent = 0
        total_per_week_actbudget_percent = 0
        table = []

        while week_start_date < last_date_report:
            week_number = week_number + 1
            week_str = "W%d" % week_number
            row = {'week': week_str}

            week_start_date_new = project_start_date + timedelta(days=add7days)
            wsd = week_start_date_new.strftime("%d %b, %Y")
            row.update({'week_start_date': wsd})

            if week_str == 'W1':
                addtoenddate = addtoenddate + 6
                week_end_date = project_start_date + timedelta(days=addtoenddate)
                wed = week_end_date.strftime("%d %b, %Y")
            else:
                addtoenddate = addtoenddate + 7
                week_end_date = project_start_date + timedelta(days=addtoenddate)
                wed = week_end_date.strftime("%d %b, %Y")
            row.update({'week_end_date': wed})

            per_week_budget = 0
            per_week_budget_percent = 0
            per_week_actbudget = 0
            per_week_actbudget_percent = 0
            for jobcost_sheet in job_cost_sheets:
                for task in jobcost_sheet.task_id:
                    # for rec_task in task:
                    task_start_date = datetime.strptime(task.start_date, '%Y-%m-%d %H:%M:%S').date()
                    task_end_date = datetime.strptime(task.p_end_date, '%Y-%m-%d %H:%M:%S').date()
                    if week_end_date >= task_start_date >= week_start_date_new:
                        task_in_week = ((week_end_date - task_start_date) + timedelta(days=1)).days
                        # per_day planned budget amount
                        per_day_budget = self.get_each_day_budget(task)
                        each_day_budget_week = per_day_budget * task_in_week
                        per_week_budget += each_day_budget_week
                        # per day planned budget amount in percentage
                        per_day_budget_per = self.get_each_day_budget_per(per_day_budget)
                        each_day_budget_week_percent = per_day_budget_per * task_in_week
                        per_week_budget_percent += each_day_budget_week_percent
                        # Per day Actual budget amount and Per day actual budget amount in percentage
                        pd_actu_bud_dict = self.get_actual_budget(task)
                        eachd_actual_budget_week = pd_actu_bud_dict.get("per_day_actual_budget") * task_in_week
                        per_week_actbudget = per_week_actbudget + eachd_actual_budget_week
                        each_day_act_budget_week_percent = pd_actu_bud_dict.get(
                            "pday_actual_budget_percentage") * task_in_week
                        per_week_actbudget_percent = per_week_actbudget_percent + each_day_act_budget_week_percent
                    elif week_end_date >= task_end_date >= week_start_date_new:
                        task_in_week_1 = ((task_end_date - week_start_date_new) + timedelta(days=1)).days
                        per_day_budget_1 = self.get_each_day_budget(task)
                        each_day_budget_week_1 = per_day_budget_1 * task_in_week_1
                        per_week_budget = per_week_budget + each_day_budget_week_1

                        per_day_budget_per_1 = self.get_each_day_budget_per(per_day_budget_1)
                        each_day_budget_week_percent_1 = per_day_budget_per_1 * task_in_week_1
                        per_week_budget_percent = per_week_budget_percent + each_day_budget_week_percent_1
                        # Per day Actual budget amount and Per day actual budget amount in percentage
                        pd_actu_bud_dict_1 = self.get_actual_budget(task)
                        eachd_actual_budget_week_1 = pd_actu_bud_dict_1.get("per_day_actual_budget") * task_in_week_1
                        per_week_actbudget = per_week_actbudget + eachd_actual_budget_week_1
                        each_day_act_budget_week_percent_1 = pd_actu_bud_dict_1.get(
                            "pday_actual_budget_percentage") * task_in_week_1
                        per_week_actbudget_percent = per_week_actbudget_percent + each_day_act_budget_week_percent_1

            per_week_budget_str = '{:0,.2f}'.format(per_week_budget)
            total_planned_budget_each_week = total_planned_budget_each_week + per_week_budget
            total_pbew_str = '{:0,.2f}'.format(total_planned_budget_each_week)
            row.update({'planned_budget': per_week_budget_str})
            row.update({'total_planned_budget': total_pbew_str})

            per_week_budget_percent_str = "%.2f" % per_week_budget_percent + "%"
            total_per_week_budget_percent = total_per_week_budget_percent + per_week_budget_percent
            total_pwbp_str = "%.2f" % total_per_week_budget_percent + "%"
            row.update({"planned_budget_percent": per_week_budget_percent_str})
            row.update({"total_planned_budget_percent": total_pwbp_str})

            per_week_actbudget_str = '{:0,.2f}'.format(per_week_actbudget)
            total_actual_budget_each_week = total_actual_budget_each_week + per_week_actbudget
            total_abew_str = '{:0,.2f}'.format(total_actual_budget_each_week)
            row.update({'actual_budget': per_week_actbudget_str})
            row.update({'total_actual_budget': total_abew_str})

            per_week_actbudget_percent_str = "%.2f" % per_week_actbudget_percent + "%"
            total_per_week_actbudget_percent = total_per_week_actbudget_percent + per_week_actbudget_percent
            total_pwap_str = "%.2f" % total_per_week_actbudget_percent + "%"
            row.update({"actual_budget_percent": per_week_actbudget_percent_str})
            row.update({"total_actual_budget_percent": total_pwap_str})

            table.append(row)
            add7days = add7days + 7
            week_start_date = week_start_date_new

        if len(table):
            table.pop()
        else:
            raise ValidationError("Project start date and end date both not valid!")
        return table
