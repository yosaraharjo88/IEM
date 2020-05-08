odoo.define('project_management_reports.project_progress_table', function(require) {
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
    var _t = core._t;
    var _lt = core._lt;
    var QWeb = core.qweb;

    var Project_progress_table = View.extend({
        display_name: _lt('Project Progress Table'),
        icon: 'fa-columns',
        template: 'ProjectProgressTableView',
        view_type: 'project_progress_table',

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
                console.log("Project not selected.")
            }
        },

        init: function() {
            var self = this;
            this._super.apply(this, arguments);
            if (self.ViewManager.action.xml_id == "project_management_report.project_progress_report-action") {
                var check = $("#selUsers").select2();
                var username = $('#selUser option:selected').text();
                var userid = $('#selUser').val();
                var rec = new Model('project.project').call("search_read", [
                    []
                ]).then(function(projects) {
                    $.each(projects, function(index, value) {
                        $("#option_project").after(QWeb.render('project_lists', {
                            widget: this,
                            project_line: value
                        }));
                    });
                });
            }
            //Container Render.
            self.$el.html(QWeb.render('ProjectProgressTableView.main', {
                'title': "My Table",
                'widget': self,
                'display_name': this.display_name,
            }));
        },

        willStart: function() {
            if (this.ViewManager.action.xml_id == "project_management_report.project_progress_report-action") {
                console.log("When 'project_progress_report-action' action occurs.")
            } else {
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
            }
            return this._super();
        },
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
                console.log("Project Progress Table | Render Buttons Fun | Else")
            }
        },
    });
    core.view_registry.add('project_progress_table', Project_progress_table)
    return Project_progress_table;
});