odoo.define('project_budget_scurve_report.project_budget_table', function(require) {
    "use strict";

    var core = require('web.core');
    var formats = require('web.formats');
    var Model = require('web.Model');
    var data = require('web.data');
    var time = require('web.time');
    var View = require('web.View');
    var form_common = require('web.form_common');
    var Dialog = require('web.Dialog');
    var utils = require('web.utils');
    var session = require('web.session');
    var framework = require('web.framework');
    var session = require('web.session');
    var _t = core._t;
    var _lt = core._lt;
    var QWeb = core.qweb;

    var Project_budget_table = View.extend({
        display_name: _lt('Project Budget Table'),
        icon: 'fa-columns',
        template: 'ProjectBudgetView',
        view_type: 'project_budget_table',

        init: function() {
            var self = this;
            this._super.apply(this, arguments);
            //Container Render.
            if (self.ViewManager.action.xml_id == "project_budget_scurve_report.project_budget_report-action") {
                var check = $("#selUser").select2();
                var rec = new Model('project.project').call("search_read", [
                    []
                ]).then(function(projects) {
                    $.each(projects, function(index, value) {
                        $("#option_project").after(QWeb.render('project_lists', {
                            widget: this,
                            project_line: value,
                        }));
                    });
                });
                var username = $('#selUser option:selected').text();
                var userid = $('#selUser').val();
            }
            self.$el.html(QWeb.render('ProjectBudgetView.main', {
                'title': "My Table",
                'widget': self,
                'display_name': this.display_name,
            }));
        },

        render_buttons: function($node) {
            if (this.ViewManager.action.xml_id == "project_budget_scurve_report.project_budget_report-action") {
                if ($node) {
                    var context = {
                        measures: _.pairs(_.omit(this.measures, '__count__'))
                    };
                    this.$buttons = $(QWeb.render('ProjectProgressTableView.buttons', context));
                    this.$buttons.click(this.onClickSelectProject.bind(this));
                    this.$buttons.appendTo($node);
                }
            } else {
                console.log("Project Budget Table | Render Buttons Fun | Else")
            }
        },

        onClickSelectProject: function() {
            var check = $("#selUser").select2();
            var username = $('#selUser option:selected').text();
            var userid = $('#selUser').val();
            sessionStorage.setItem("SessionName",userid);
            if (parseInt(userid) > 0) {
                var get_values = new Model('project.project').call("get_project_budget_data", [
                    [parseInt(userid)]
                ]).then(function(result) {
                    var table = self.google.charts.load('current', {
                        'packages': ['table']
                    }).then(function() {
                        var data = new self.google.visualization.DataTable();
                        data.addColumn('string', 'Period');
                        data.addColumn('string', 'Start Date');
                        data.addColumn('string', 'End Date');
                        data.addColumn('number', 'Planned Budget');
                        data.addColumn('number', 'Planned Budget (%)');
                        data.addColumn('number', 'Total Planned Budget');
                        data.addColumn('number', 'Total Planned Budget (%)');
                        data.addColumn('number', 'Actual Budget');
                        data.addColumn('number', 'Actual Budget (%)');
                        data.addColumn('number', 'Total Actual Budget');
                        data.addColumn('number', 'Total Actual Budget (%)');
                        var rec;
                        for (rec = 0; rec < result.length; rec++) {
                            data.addRows([
                                [result[rec].week, result[rec].week_start_date, result[rec].week_end_date, {
                                    f: result[rec].planned_budget
                                }, {
                                    f: result[rec].planned_budget_percent
                                }, {
                                    f: result[rec].total_planned_budget
                                }, {
                                    f: result[rec].total_planned_budget_percent
                                }, {
                                    f: result[rec].actual_budget
                                }, {
                                    f: result[rec].actual_budget_percent
                                }, {
                                    f: result[rec].total_actual_budget
                                }, {
                                    f: result[rec].total_actual_budget_percent
                                }, ]
                            ]);
                        }
                        var load = self.google.charts.setOnLoadCallback(data);
                        var draw_table = new google.visualization.Table(document.getElementById('project_report_bg_color'));
                        draw_table.draw(data, {
                            width: '100%',
                        });
                    });
                });
            } else {
                console.log("Project not selected.")
            }
        },
    });

    core.view_registry.add('project_budget_table', Project_budget_table)
    return Project_budget_table;
});