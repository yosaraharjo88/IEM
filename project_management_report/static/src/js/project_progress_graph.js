odoo.define('project_management_reports.project_progress_graph', function(require) {
    "use strict";

    var core = require('web.core');
    var View = require('web.View');
    var Model = require('web.Model');
    var QWeb = core.qweb;
    var _lt = core._lt;

    var Project_progress_graph = View.extend({
        display_name: _lt('S-curve Graph'),
        icon: 'fa-area-chart',
        template: 'ProjectProgressGraphView',
        view_type: 'projectprogressgraph',

        init: function() {
            var self = this;
            this._super.apply(this, arguments);
            if (self.ViewManager.action.xml_id == "project_management_report.project_progress_report-action") {
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
            //Container Render.
            this.$el.html(QWeb.render('ProjectProgressGraphView.main', {
                'title': "My Graph",
                'widget': self,
                'display_name': this.display_name,
            }));
        },

        willStart: function() {
            if (this.ViewManager.action.xml_id == "project_management_report.project_progress_report-action") {
                console.log("Project progress graph | When 'project_progress_report-action' action occurs.")
            } else {
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

            }
            return this._super();
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
                console.log("Project Progress Graph | Render Buttons Fun | Else")
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
                console.log("Project not selected.")
            }
        },
    });
    core.view_registry.add('projectprogressgraph', Project_progress_graph)
    return Project_progress_graph;
});