odoo.define('project_budget_scurve_report.project_budget_buttons_table', function(require) {
    "use strict";

    var core = require('web.core');
    var Model = require('web.Model');
    var Project_Progress_Table = require('project_management_reports.project_progress_table');
    var QWeb = core.qweb;

    Project_Progress_Table.include({
        render_buttons: function($node) {
            if (this.ViewManager.action.xml_id == "project_management_report.project_progress_report-action") {
                if ($node) {
                    var context = {
                        measures: _.pairs(_.omit(this.measures, '__count__'))
                    };
                    this.$buttons = $(QWeb.render('ProjectProgressTableView.buttons', context));
                    this.$buttons.click(this.onClickSelectProject.bind(this));
                    this.$buttons.appendTo($node);
                }
            } else {
                if ($node) {
                    var context = {
                        measures: _.pairs(_.omit(this.measures, '__count__'))
                    };
                    this.$buttons = $(QWeb.render('SelectProjectBudget_buttons', context));
                    this.$buttons.click(this.onClickSelectProject.bind(this));
                    this.$buttons.appendTo($node);
                }
            }
        },

        SelectProjectButton: function(events) {
            var pass = new Model('project.project').call("gen_table", [
                [parseInt(this.dataset.context.active_id)]
            ]).then(function(result) {
                var table = self.google.charts.load('current', {
                    'packages': ['table']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', 'Period');
                    data.addColumn('string', 'Start Date');
                    data.addColumn('string', 'End Date');
                    data.addColumn('number', 'Planned Progress');
                    data.addColumn('number', 'Total Planned Progress');
                    data.addColumn('number', 'Actual Progress');
                    data.addColumn('number', 'Total Actual Progress');
                    var rec;
                    for (rec = 0; rec < result.length; rec++) {
                        data.addRows([
                            [result[rec].week, result[rec].week_start_date, result[rec].week_end_date, {
                                f: result[rec].planned_progress
                            }, {
                                f: result[rec].total_planned_progress
                            }, {
                                f: result[rec].actual_planned_progress
                            }, {
                                f: result[rec].total_actual_progress
                            }],
                        ]);
                    }
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.Table(document.getElementById('project_report_bg_color'));
                    draw_table.draw(data, {
                        width: '100%',
                    });
                });
            });
        },

        SelectBudgetButtons: function(events) {
            if (parseInt(this.dataset.context.active_id) > 0) {
                var get_values = new Model('project.project').call("get_project_budget_data", [
                    [parseInt(this.dataset.context.active_id)]
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
            }
        },

        onClickSelectProject: function(events) {
            var check = $("#selUser").select2();
            var username = $('#selUser option:selected').text();
            var userid = $('#selUser').val();
            if (parseInt(userid) > 0) {
                var pass = new Model('project.project').call("gen_table", [
                    [parseInt(userid)]
                ]).then(function(result) {
                    var table = self.google.charts.load('current', {
                        'packages': ['table']
                    }).then(function() {
                        var data = new self.google.visualization.DataTable();
                        data.addColumn('string', 'Period');
                        data.addColumn('string', 'Start Date');
                        data.addColumn('string', 'End Date');
                        data.addColumn('number', 'Planned Progress');
                        data.addColumn('number', 'Total Planned Progress');
                        data.addColumn('number', 'Actual Progress');
                        data.addColumn('number', 'Total Actual Progress');
                        var rec;
                        for (rec = 0; rec < result.length; rec++) {
                            data.addRows([
                                [result[rec].week, result[rec].week_start_date, result[rec].week_end_date, {
                                    f: result[rec].planned_progress
                                }, {
                                    f: result[rec].total_planned_progress
                                }, {
                                    f: result[rec].actual_planned_progress
                                }, {
                                    f: result[rec].total_actual_progress
                                }],
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
                var $target = $(event.target);
                if ($(event.target).attr('id') == 'select_project_button') {
                    return this.SelectProjectButton();
                }
                if ($(event.target).attr('id') == 'select_budget_button') {
                    return this.SelectBudgetButtons();
                }
            }
        },
    })
});