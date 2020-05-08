odoo.define('project_budget_scurve_report.project_budget_buttons_graph', function(require) {
    "use strict";

    var core = require('web.core');
    var Model = require('web.Model');
    var View = require('web.View');
    var Project_Progress_Graph = require('project_management_reports.project_progress_graph');
    var QWeb = core.qweb;

    Project_Progress_Graph.include({

        // Generate graph of Planned progress VS Actual progress of Project
        SelectProjectButtonGraph: function(events) {
            var pass = new Model('project.project').call("gen_table", [
                [parseInt(this.dataset.context.active_id)]
            ]).then(function(result) {
                var graph = self.google.charts.load('current', {
                    'packages': ['corechart']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', 'Weeks'); // Implicit domain label col.
                    data.addColumn('number', 'Planned Progress'); // Implicit series 1 data col.
                    data.addColumn('number', 'Actual Progress');
                    var rec;
                    for (rec = 0; rec < result.length; rec++) {
                        data.addRows([
                            [result[rec].week, parseFloat(result[rec].total_planned_progress), parseFloat(result[rec].total_actual_progress)],
                        ]);
                    }
                    var options = {
                        title: 'Project Progress Report',
                        curveType: 'function',
                        legend: {
                            position: 'bottom'
                        }
                    };
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.LineChart(document.getElementById('project_progress_graph_bg_color'));
                    draw_table.draw(data, options);
                });
            });
        },

        // Generate graph of Planned Budget VS Actual Budget for project
        SelectBudgetButtonsGraph: function(events) {
            if (parseInt(this.dataset.context.active_id) > 0) {
                var val = new Model('project.project').call("get_project_budget_data", [
                    [parseInt(this.dataset.context.active_id)]
                ]).then(function(result) {
                    var graph = self.google.charts.load('current', {
                        'packages': ['corechart']
                    }).then(function() {
                        var data = new self.google.visualization.DataTable();
                        data.addColumn('string', 'Weeks'); // Implicit domain label col.
                        data.addColumn('number', 'Planned Budget'); // Implicit series 1 data col.
                        data.addColumn('number', 'Actual Budget');
                        var rec;
                        for (rec = 0; rec < result.length; rec++) {
                            data.addRows([
                                [result[rec].week, parseFloat(result[rec].total_planned_budget_percent), parseFloat(result[rec].total_actual_budget_percent)]
                            ])
                        }
                        var options = {
                            title: 'Project Planned Budget vs Actual Budget Graph Report',
                            curveType: 'function',
                            legend: {
                                position: 'bottom'
                            }
                        };
                        var load = self.google.charts.setOnLoadCallback(data);
                        var draw_table = new google.visualization.LineChart(document.getElementById('project_progress_graph_bg_color'));
                        draw_table.draw(data, options);
                    });
                });
            }
        },

        onClickSelectProjects: function(events) {
            var check = $("#selUser").select2();
            var username = $('#selUser option:selected').text();
            var userid = $('#selUser').val();
            if (parseInt(userid) > 0) {
                var val = new Model('project.project').call("gen_table", [
                    [parseInt(userid)]
                ]).then(function(result) {
                    var graph = self.google.charts.load('current', {
                        'packages': ['corechart']
                    }).then(function() {
                        var data = new self.google.visualization.DataTable();
                        data.addColumn('string', 'Weeks'); // Implicit domain label col.
                        data.addColumn('number', 'Planned Progress'); // Implicit series 1 data col.
                        data.addColumn('number', 'Actual Progress');
                        var rec;
                        for (rec = 0; rec < result.length; rec++) {
                            data.addRows([
                                [result[rec].week, parseFloat(result[rec].total_planned_progress), parseFloat(result[rec].total_actual_progress)],
                            ]);
                        }
                        var options = {
                            title: 'Project Progress Report',
                            curveType: 'function',
                            legend: {
                                position: 'bottom'
                            }
                        };
                        var load = self.google.charts.setOnLoadCallback(data);
                        var draw_table = new google.visualization.LineChart(document.getElementById('project_progress_graph_bg_color'));
                        draw_table.draw(data, options);
                    });
                });
            } else {
                var $target = $(event.target);
                if ($(event.target).attr('id') == 'select_project_button') {
                    return this.SelectProjectButtonGraph();
                }
                if ($(event.target).attr('id') == 'select_budget_button') {
                    return this.SelectBudgetButtonsGraph();
                }
            }
        },

        render_buttons: function($node) {
            if (this.ViewManager.action.xml_id == "project_management_report.project_progress_report-action") {
                if ($node) {
                    var context = {
                        measures: _.pairs(_.omit(this.measures, '__count__'))
                    };
                    this.$buttons = $(QWeb.render('ProjectProgressGraphView.buttons', context));
                    this.$buttons.click(this.onClickSelectProjects.bind(this));
                    this.$buttons.appendTo($node);
                }
            } else {
                if ($node) {
                    var context = {
                        measures: _.pairs(_.omit(this.measures, '__count__'))
                    };
                    this.$buttons = $(QWeb.render('SelectProjectBudget_buttons', context));
                    this.$buttons.click(this.onClickSelectProjects.bind(this));
                    this.$buttons.appendTo($node);
                }
            }
        }
    })
});