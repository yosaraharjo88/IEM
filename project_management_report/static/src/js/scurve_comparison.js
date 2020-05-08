odoo.define('project_management_reports.scurve_comparison', function(require) {
    "use strict";

    var core = require('web.core');
    var View = require('web.View');
    var Model = require('web.Model');
    var _lt = core._lt;
    var QWeb = core.qweb;


    var SCurve_comparison_view = View.extend({
        display_name: _lt('S-curve Comparison'),
        icon: 'fa-line-chart',
        template: 'ScurveComparisonView',
        view_type: 'scurvecomparison',

        events: {
            'click .checkbox': 'onClickPlannedActual',
        },

        //        When select both
        SelectPlannedActualBoth: function(active_id) {
            var d = new Date();
            var pass = new Model('project.project').call("gen_table", [
                [parseInt(active_id)]
            ]).then(function(result) {
                // for preparing Graph
                var graph = self.google.charts.load('current', {
                    'packages': ['corechart']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', 'Weeks'); // Implicit domain label col.
                    data.addColumn('number', 'Planned Progress'); // Implicit series 1 data col.
                    data.addColumn('number', 'Actual Progress');
                    data.addColumn({
                        type: 'boolean',
                        role: 'scope'
                    }); // scope col.
                    var rec;
                    for (rec = 0; rec < result.length; rec++) {
                        var dt = new Date(result[rec].week_end_date);
                        if (d <= dt) {
                            var check = false;
                        } else {
                            var check = true;
                        }
                        data.addRows([
                            [result[rec].week, parseFloat(result[rec].total_planned_progress), parseFloat(result[rec].total_actual_progress), check],
                        ]);
                    }
                    var options = {
                        title: 'Project Progress Report',
                        curveType: 'function',
                        backgroundColor: '#f0eeee',
                        legend: {
                            position: 'bottom'
                        }
                    };
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.LineChart(document.getElementById('scurve_comparison_chart'));
                    draw_table.draw(data, options);
                });
                //                            for preparing Table
                var table = self.google.charts.load('current', {
                    'packages': ['table']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', '');
                    var rec;
                    var planned_progress = ['Planned Progress']
                    var actual_progress = ['Actual Progress']
                    for (rec = 0; rec < result.length; rec++) {
                        data.addColumn('string', result[rec].week);
                        planned_progress.push(result[rec].total_planned_progress);
                        actual_progress.push(result[rec].total_actual_progress);
                    }
                    data.addRows([planned_progress, actual_progress]);
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.Table(document.getElementById('scurve_comparison_table'));
                    draw_table.draw(data, {
                        //showRowNumber: true,
                        backgroundColor: '#f0eeee',
                        width: '100%',
                        //height: '15%'
                    });
                });
            });
        },

        //        When Planned Progress is checked
        SelectPlannedProgress: function(active_id) {
            var pass = new Model('project.project').call("gen_table", [
                [parseInt(active_id)]
            ]).then(function(result) {
                //                            for preparing Graph
                var graph = self.google.charts.load('current', {
                    'packages': ['corechart']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', 'Weeks'); // Implicit domain label col.
                    data.addColumn('number', 'Planned Progress'); // Implicit series 1 data col.
                    var rec;
                    for (rec = 0; rec < result.length; rec++) {
                        data.addRows([
                            [result[rec].week, parseFloat(result[rec].total_planned_progress)],
                        ]);
                    }
                    var options = {
                        title: 'Project Progress Report',
                        curveType: 'function',
                        backgroundColor: '#f0eeee',
                        legend: {
                            position: 'bottom'
                        }
                    };
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.LineChart(document.getElementById('scurve_comparison_chart'));
                    draw_table.draw(data, options);
                });
                //                            for preparing Table
                var table = self.google.charts.load('current', {
                    'packages': ['table']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', '');
                    var rec;
                    var planned_progress = ['Planned Progress']
                    for (rec = 0; rec < result.length; rec++) {
                        data.addColumn('string', result[rec].week);
                        planned_progress.push(result[rec].total_planned_progress);
                    }
                    data.addRows([planned_progress]);
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.Table(document.getElementById('scurve_comparison_table'));
                    draw_table.draw(data, {
                        //showRowNumber: true,
                        backgroundColor: '#f0eeee',
                        width: '100%',
                        //height: '15%'
                    });
                });
            });
        },

        //        When Actual is checked
        SelectActualProgress: function(active_id) {
            var d = new Date();
            var pass = new Model('project.project').call("gen_table", [
                [parseInt(active_id)]
            ]).then(function(result) {
                // for actual graph preparing
                var graph = self.google.charts.load('current', {
                    'packages': ['corechart']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', 'Weeks'); // Implicit domain label col.
                    data.addColumn('number', 'Actual Progress'); // Implicit series 1 data col.
                    data.addColumn({
                        type: 'boolean',
                        role: 'scope'
                    }); // scope col.
                    var rec;
                    for (rec = 0; rec < result.length; rec++) {
                        var dt = new Date(result[rec].week_end_date);
                        if (d <= dt) {
                            var check = false;
                        } else {
                            var check = true;
                        }
                        data.addRows([
                            [result[rec].week, parseFloat(result[rec].total_actual_progress), check],
                        ]);
                    }
                    var options = {
                        title: 'Project Progress Report',
                        series: {
                            0: {
                                color: '#e2431e'
                            }
                        },
                        curveType: 'function',
                        backgroundColor: '#f0eeee',
                        legend: {
                            position: 'bottom'
                        }
                    };
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.LineChart(document.getElementById('scurve_comparison_chart'));
                    draw_table.draw(data, options);
                });
                // for actual Table preparing
                var table = self.google.charts.load('current', {
                    'packages': ['table']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', '');
                    var rec;
                    var actual_progress = ['Actual Progress']
                    for (rec = 0; rec < result.length; rec++) {
                        data.addColumn('string', result[rec].week);
                        actual_progress.push(result[rec].total_actual_progress);
                    }
                    data.addRows([actual_progress]);
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.Table(document.getElementById('scurve_comparison_table'));
                    draw_table.draw(data, {
                        backgroundColor: '#f0eeee',
                        width: '100%',
                    });
                });
            });
        },

        onClickPlannedActual: function(event) {
            var active = this.dataset.context.active_id
            // When both are TRUE
            if ($("#first_check:checked,#second_check:checked").length == 2) {
                return this.SelectPlannedActualBoth(active);
            }
            // When both are False
            if ($("#first_check:checked,#second_check:checked").length == 0) {
                alert("Please select at least one!");
                $(event.target).context.checked = true;
            }
            //            When each of then is true of false
            if ($("#first_check:checked,#second_check:checked").length == 1) {
                if ($("#first_check").prop("checked") == true) {
                    return this.SelectPlannedProgress(active);
                }
                if ($("#second_check").prop("checked") == true) {
                    return this.SelectActualProgress(active);
                }
            }
        },

        init: function() {
            var self = this;
            this._super.apply(this, arguments);
            //Container Render.
            this.$el.html(QWeb.render('ScurveComparisonView_main', {
                'title': "My Graph",
                'widget': self,
                'display_name': this.display_name,
            }));
        },

        willStart: function() {
            this.SelectPlannedActualBoth(this.dataset.context.active_id);
            return this._super();
        },
    });
    core.view_registry.add('scurvecomparison', SCurve_comparison_view);
    return SCurve_comparison_view;
});