odoo.define('project_budget_scurve_report.project_budget_graph', function(require) {
    "use strict";

    var core = require('web.core');
    var View = require('web.View');
    var Model = require('web.Model');

    var QWeb = core.qweb;
    var _lt = core._lt;

    var Project_budget_graph = View.extend({

        display_name: _lt('Project Budget Graph'),
        icon: 'fa-area-chart',
        template: 'ProjectBudgetGraphView',
        view_type: 'project_budget_graph',

        init: function() {
            var self = this;
            this._super.apply(this, arguments);
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
            self.$el.html(QWeb.render('ProjectBudgetGraphView.main', {
                'title': "My Graph",
                'widget': self,
                'display_name': this.display_name,
            }));
        },

        willStart: function() {
            if (this.ViewManager.action.xml_id == "project_budget_scurve_report.project_budget_report-action") {
                var get_user_id = sessionStorage.getItem("SessionName");
                if (get_user_id) {
                    var val = new Model('project.project').call("get_project_budget_data", [
                        [parseInt(get_user_id)]
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
                            var draw_table = new google.visualization.LineChart(document.getElementById('project_budget_graph_report_bg_color'));
                            draw_table.draw(data, options);
                        });
                    });
                    sessionStorage.removeItem('SessionName');
                } else {
                    console.log("Session not found")
                }
            }
            return this._super();
        },

        render_buttons: function($node) {
            if (this.ViewManager.action.xml_id == "project_budget_scurve_report.project_budget_report-action") {
                if ($node) {
                    var context = {
                        measures: _.pairs(_.omit(this.measures, '__count__'))
                    };
                    this.$buttons = $(QWeb.render('ProjectProgressGraphView.buttons', context));
                    this.$buttons.click(this.onClickSelectProjectBudget.bind(this));
                    this.$buttons.appendTo($node);
                }
            } else {
                console.log("Project Budget Graph | Render Buttons Fun | Else")
            }
        },

        onClickSelectProjectBudget: function() {
            var check = $("#selUser").select2();
            var username = $('#selUser option:selected').text();
            var userid = $('#selUser').val();
            if (parseInt(userid) > 0) {
                var val = new Model('project.project').call("get_project_budget_data", [
                    [parseInt(userid)]
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
                        var draw_table = new google.visualization.LineChart(document.getElementById('project_budget_graph_report_bg_color'));
                        draw_table.draw(data, options);
                    });
                });
            } else {
                console.log("Project not selected.")
            }
        },

    });

    core.view_registry.add('project_budget_graph', Project_budget_graph)
    return Project_budget_graph;

});