import logging
from odoo import api, fields, models
from odoo.exceptions import ValidationError

from datetime import datetime
from datetime import timedelta

_logger = logging.getLogger(__name__)


class ProjectProjectInherit(models.Model):
    _inherit = 'project.project'


    def gen_table(self):
        if self.project_start_date:
            project_start_date = datetime.strptime(self.project_start_date, '%Y-%m-%d %H:%M:%S').date()
        else:
            raise ValidationError("Project Start Date not found!")
        if not self.project_end_date:
            raise ValidationError("Project End Date not found!")
        project_end_date = datetime.strptime(self.project_end_date, '%Y-%m-%d %H:%M:%S').date()

        add7days = 0
        week_start_date = project_start_date
        week_number = 0
        addtoenddate = 0

        table = []
        total_planned_progress_each_week = 0
        total_actual_prog_p_week = 0

        while week_start_date < project_end_date:
            week_number += 1
            week_str = "W%d" % week_number
            # _logger.info(["Generate Table | Week: ", week_str])
            row = {'week': week_str}

            project_start_date_new = project_start_date + timedelta(days=add7days)
            wsd = project_start_date_new.strftime("%d %b, %Y")
            row.update({'week_start_date': wsd})

            if week_str == 'W1':
                addtoenddate += 6
                week_end_date = project_start_date + timedelta(days=addtoenddate)
                wed = week_end_date.strftime("%d %b, %Y")
            else:
                addtoenddate = addtoenddate + 7
                week_end_date = project_start_date + timedelta(days=addtoenddate)
                wed = week_end_date.strftime("%d %b, %Y")
            row.update({'week_end_date': wed})

            plan_prog_p_week = 0
            actual_prog_p_week = 0
            for rec_task in self.tasks:
                if not rec_task.start_date:
                    raise ValidationError("Start date of '%s' task not found!" % rec_task.name)
                else:
                    task_start_date = datetime.strptime(rec_task.start_date, '%Y-%m-%d %H:%M:%S').date()
                if not rec_task.p_end_date:
                    raise ValidationError("End date of '%s' task not found!" % rec_task.name)
                else:
                    task_end_date = datetime.strptime(rec_task.p_end_date, '%Y-%m-%d %H:%M:%S').date()
                task_duration = ((task_end_date - task_start_date) + timedelta(days=1)).days
                # Check Task with start date
                if week_end_date >= task_start_date >= project_start_date_new:
                    # how many day occurs task in week
                    task_in_week = ((week_end_date - task_start_date) + timedelta(days=1)).days
                    for project_stage in self.project_stage_ids:
                        if rec_task.stage_id.id == project_stage.type_id.id:
                            # Planned Progress calculation for each day per each task
                            each_day_planned = (((project_stage.stage_weightage * rec_task.planned_progress) / 100)
                                                / task_duration)
                            each_day_planned_in_week = each_day_planned * task_in_week
                            plan_prog_p_week = plan_prog_p_week + each_day_planned_in_week
                # Check task with End date
                elif week_end_date >= task_end_date >= project_start_date_new:
                    task_in_week_2 = ((task_end_date - project_start_date_new) + timedelta(days=1)).days
                    for project_stage_2 in self.project_stage_ids:
                        if rec_task.stage_id.id == project_stage_2.type_id.id:
                            each_day_planned_2 = (((project_stage_2.stage_weightage * rec_task.planned_progress)
                                                   / 100) / task_duration)
                            each_day_planned_2_in_week = each_day_planned_2 * task_in_week_2
                            plan_prog_p_week = plan_prog_p_week + each_day_planned_2_in_week

                elif project_start_date_new >= task_start_date and week_end_date <= task_end_date:
                    # count days which not consider in week after week end date
                    a = (task_end_date - week_end_date).days
                    # count days which not consider in week before week start date
                    b = (project_start_date_new - task_start_date).days
                    # Total days which not consider in week
                    c = a + b
                    task_in_week_3 = task_duration - c
                    for project_stage_3 in self.project_stage_ids:
                        if rec_task.stage_id.id == project_stage_3.type_id.id:
                            each_day_planned_3 = (((project_stage_3.stage_weightage * rec_task.planned_progress)
                                                   / 100) / task_duration)
                            each_day_planned_3_in_week = each_day_planned_3 * task_in_week_3
                            plan_prog_p_week = plan_prog_p_week + each_day_planned_3_in_week

                for history in rec_task.task_progress_ids:
                    if not history.progress_start_date:
                        ValidationError("Progress history details not found proper of the %s task" % rec_task.name)
                    pro_his_start_date = datetime.strptime(history.progress_start_date, '%Y-%m-%d %H:%M:%S').date()

                    if not history.progress_end_date:
                        ValidationError("Progress history details not found proper of the %s task" % rec_task.name)
                    pro_his_end_date = datetime.strptime(history.progress_end_date, '%Y-%m-%d %H:%M:%S').date()

                    pro_his_duration = ((pro_his_end_date - pro_his_start_date) + timedelta(days=1)).days

                    # If whole history progress in a week
                    if (week_end_date >= pro_his_start_date >= project_start_date_new) and (
                            week_end_date >= pro_his_end_date >= project_start_date_new):
                        for stage_weightage in self.project_stage_ids:
                            if rec_task.stage_id.id == stage_weightage.type_id.id:
                                stage_task_weightage_100 = (
                                        (stage_weightage.stage_weightage * rec_task.planned_progress) / 100)
                                progress_dur = (history.additional_progress / pro_his_duration)

                                new_each_day_act_planned = (stage_task_weightage_100 * progress_dur) / 100
                                actual_prog_p_week = actual_prog_p_week + new_each_day_act_planned

                    # for when progress history in one and more weeks.
                    elif week_end_date >= pro_his_start_date >= project_start_date_new:
                        pro_his_in_week = ((week_end_date - pro_his_start_date) + timedelta(days=1)).days
                        for stage_weightage_1 in self.project_stage_ids:
                            if rec_task.stage_id.id == stage_weightage_1.type_id.id:
                                stage_task_weightage_100_1 = (
                                        (stage_weightage_1.stage_weightage * rec_task.planned_progress) / 100)
                                progress_dur_1 = (history.additional_progress / pro_his_duration)
                                new_each_day_act_planned_1 = (stage_task_weightage_100_1 * progress_dur_1) / 100
                                actual_plan_per_week = new_each_day_act_planned_1 * pro_his_in_week
                                actual_prog_p_week = actual_prog_p_week + actual_plan_per_week
                    elif week_end_date >= pro_his_end_date >= project_start_date_new:
                        pro_his_in_week_1 = ((pro_his_end_date - project_start_date_new) + timedelta(days=1)).days
                        for stage_weightage_2 in self.project_stage_ids:
                            if rec_task.stage_id.id == stage_weightage_2.type_id.id:
                                stage_task_weightage_100_2 = (
                                        (stage_weightage_2.stage_weightage * rec_task.planned_progress) / 100)
                                progress_dur_2 = (history.additional_progress / pro_his_duration)
                                new_each_day_act_planned_2 = (stage_task_weightage_100_2 * progress_dur_2) / 100
                                actual_plan_per_week_1 = new_each_day_act_planned_2 * pro_his_in_week_1
                                actual_prog_p_week = actual_prog_p_week + actual_plan_per_week_1

            plan_prog_p_week_str = "%.2f" % plan_prog_p_week + "%"
            total_planned_progress_each_week = total_planned_progress_each_week + plan_prog_p_week
            total_ppew_str = "%.2f" % total_planned_progress_each_week + "%"
            row.update({'planned_progress': plan_prog_p_week_str})
            row.update({'total_planned_progress': total_ppew_str})

            actual_prog_p_week_str = "%.2f" % actual_prog_p_week + "%"
            total_actual_prog_p_week = total_actual_prog_p_week + actual_prog_p_week
            total_actual_prog_p_week_str = "%.2f" % total_actual_prog_p_week + "%"
            row.update({'actual_planned_progress': actual_prog_p_week_str})
            row.update({'total_actual_progress': total_actual_prog_p_week_str})

            table.append(row)
            add7days = add7days + 7
            week_start_date = project_start_date_new

        if len(table):
            table.pop()
        else:
            raise ValidationError("Project start date and end date both")
        return table

    def create_progress_history(self):
        for task_id in self.task_ids:
            for progress_history in task_id.task_progress_ids:
                if progress_history.status == "forecast" or progress_history.status == False:
                    progress_history.unlink()

            pro_his_vals = {'project_task_id': task_id.id, 'created_date': datetime.now()}
            task_end_date = datetime.strptime(task_id.p_end_date, '%Y-%m-%d %H:%M:%S')
            task_duration_p = (task_end_date - datetime.strptime(task_id.start_date, '%Y-%m-%d %H:%M:%S')).days
            add7day = timedelta(days=7)
            if not task_id.task_progress_ids:
                pro_his_vals['progress_start_date'] = datetime.now()
                end_date = pro_his_vals['progress_start_date'] + timedelta(days=task_duration_p)
                while pro_his_vals['progress_start_date'] < end_date:
                    pro_his_vals['progress_end_date'] = pro_his_vals['progress_start_date'] + timedelta(days=6)
                    pro_his_duration = (
                            (pro_his_vals['progress_end_date'] - pro_his_vals['progress_start_date']) + timedelta(
                        days=1)).days
                    pro_his_vals['additional_progress'] = (
                                                                      task_id.planned_progress / task_duration_p) * pro_his_duration
                    pro_his_vals['status'] = 'forecast'
                    task_id.task_progress_ids.create(pro_his_vals)
                    pro_his_vals['progress_start_date'] += add7day
            else:
                pro_his_vals['progress_start_date'] = datetime.strptime(
                    task_id.task_progress_ids[-1].progress_start_date,
                    '%Y-%m-%d %H:%M:%S') + add7day
                end_date = pro_his_vals['progress_start_date'] + timedelta(days=task_duration_p)
                while pro_his_vals['progress_start_date'] < end_date:
                    pro_his_vals['progress_end_date'] = pro_his_vals['progress_start_date'] + timedelta(days=6)
                    pro_his_vals['additional_progress'] = (task_id.planned_progress / task_duration_p) * (
                            (pro_his_vals['progress_end_date'] - pro_his_vals['progress_start_date']) + timedelta(
                        days=1)).days

                    pro_his_vals['status'] = 'forecast'
                    task_id.task_progress_ids.create(pro_his_vals)
                    pro_his_vals['progress_start_date'] += add7day
