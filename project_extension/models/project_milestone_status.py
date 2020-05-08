from odoo import api, fields, models, _


class ProjectMilestoneStatus(models.Model):
    _name = 'project.milestone.status'
    _rec_name = 'status_name'

    status_name = fields.Char(string="Status Name")
    status_description = fields.Text(string="Description")
    conditional_description = fields.Char(string="Conditional Description")
    color = fields.Char(string="Color")
    condition = fields.Selection([('match_all', 'Match All'), ('match_one', 'Match One')], string="Condition")
    conditional_format = fields.One2many('project.milestone.conditional.line', 'project_milestone_id',
                                         string="Conditional formatting")
    conditional_description = fields.Char(string="Conditional Description")

    @api.onchange('conditional_format')
    def onchange_conditional_description(self):
        list1 = ["If Archived Date is"]
        for rec in self.conditional_format:
            if rec.terms and rec.variable:
                list1.append(dict(rec._fields['terms'].selection).get(rec.terms))
                list1.append(dict(rec._fields['variable'].selection).get(rec.variable))
                if len(list1) > 3:
                    list1.insert(3, "and")
                des = " ".join(list1)
            self.conditional_description = des
        return


class ProjectMilestoneConditional(models.Model):
    _name = 'project.milestone.conditional.line'

    project_milestone_id = fields.Many2one('project.milestone.status', string="Milestone Status")
    terms = fields.Selection([('greater_than', 'Greater than'), ('greater_than_equal', 'Greater than or equal to'),
                              ('less_than', 'Less than'), ('less_than_equal', 'Less than or equal to'),
                              ('equal_to', 'Equal to'), ('not_equal_to', 'Not equal to')], string="Terms")
    variable = fields.Selection([('expected_date', 'Expected Date'), ('expected_date_tol', 'Expected date + Tolerance'),
                                 ('expected_date_dur', 'Expected date + Duration'),
                                 ('expected_date_tol_dur', 'Expected date + Tolerance + Duration')], string="Variable")
    duration = fields.Integer(string="Duration (days)")