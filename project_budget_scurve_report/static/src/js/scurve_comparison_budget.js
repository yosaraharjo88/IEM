odoo.define('project_budget_scurve_report.scurve_comparison_budget', function(require) {
    "use strict";

    var core = require('web.core');
    var ajax = require('web.ajax');
    var Model = require('web.Model');
    var QWeb = core.qweb;
    var Scurve_comparison_view = require('project_management_reports.scurve_comparison');

    Scurve_comparison_view.include({

        // When Planned Budget and Actual Budget
        PlannedActualBudget: function(active_id) {
            var merge_dict = new Model('project.project').call("merge_progress_budget", [
                [active_id]
            ]).then(function(result) {
                // for graph preparing
                var graph = self.google.charts.load('current', {
                    'packages': ['corechart']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', 'Weeks'); // Implicit domain label col.
                    data.addColumn('number', 'Planned Budget');
                    data.addColumn('number', 'Actual Budget');
                    var rec;
                    for (rec = 0; rec < result.length; rec++) {
                        data.addRows([
                            [result[rec].week,
                                parseFloat(result[rec].total_planned_budget_percent),
                                parseFloat(result[rec].total_actual_budget_percent),
                            ]
                        ]);
                    }
                    var options = {
                        title: 'Project Planned and Actual Budget Graph Report',
                        curveType: 'function',
                        series: {
                            0: {
                                color: '#ff9900'
                            },
                            1: {
                                color: '#109618'
                            },
                        },
                        backgroundColor: '#f0eeee',
                        legend: {
                            position: 'bottom'
                        }
                    };
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.LineChart(document.getElementById('scurve_comparison_chart'));
                    draw_table.draw(data, options);
                });
                // for table preparing
                var table = self.google.charts.load('current', {
                    'packages': ['table']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', '');
                    var rec;
                    var planned_budget = ['Planned Budget'];
                    var actual_budget = ['Actual Budget'];
                    var total_planned_budget_list = ['Total Planned Budget Amount'];
                    var total_actual_budget_list = ['Total Actual Budget Amount'];
                    for (rec = 0; rec < result.length; rec++) {
                        data.addColumn('string', result[rec].week);
                        planned_budget.push(result[rec].total_planned_budget_percent);
                        actual_budget.push(result[rec].total_actual_budget_percent);
                        total_planned_budget_list.push(result[rec].total_planned_budget);
                        total_actual_budget_list.push(result[rec].total_actual_budget);
                    }
                    data.addRows([planned_budget, total_planned_budget_list, actual_budget, total_actual_budget_list]);
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.Table(document.getElementById('scurve_comparison_table'));
                    draw_table.draw(data, {
                        backgroundColor: '#f0eeee',
                        width: '100%',
                    });
                });
            });
        },

        // When Actual Progress and Actual Budget
        ActualProgressBudget: function(active_id) {
            var d = new Date();
            var merge_dict = new Model('project.project').call("merge_progress_budget", [
                [active_id]
            ]).then(function(result) {
                // for graph preparing
                var graph = self.google.charts.load('current', {
                    'packages': ['corechart']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', 'Weeks'); // Implicit domain label col.
                    data.addColumn('number', 'Actual Progress');
                    data.addColumn({
                        type: 'boolean',
                        role: 'scope'
                    }); // scope col.
                    data.addColumn('number', 'Actual Budget');
                    var rec;
                    for (rec = 0; rec < result.length; rec++) {
                        var dt = new Date(result[rec].week_end_date);
                        if (d <= dt) {
                            var check = false;
                        } else {
                            var check = true;
                        }
                        data.addRows([
                            [result[rec].week,
                                parseFloat(result[rec].total_actual_progress),
                                check,
                                parseFloat(result[rec].total_actual_budget_percent)
                            ]
                        ]);
                    }
                    var options = {
                        title: 'Project Actual Progress and Actual Budget Graph Report',
                        curveType: 'function',
                        series: {
                            0: {
                                color: '#e2431e'
                            }, // RED color
                            1: {
                                color: '#109618'
                            }, // Green color
                        },
                        backgroundColor: '#f0eeee',
                        legend: {
                            position: 'bottom'
                        }
                    };
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.LineChart(document.getElementById('scurve_comparison_chart'));
                    draw_table.draw(data, options);
                });

                // for table preparing
                var table = self.google.charts.load('current', {
                    'packages': ['table']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', '');
                    var rec;
                    var actual_progress = ['Actual Progress'];
                    var total_actual_budget_list = ['Total Actual Budget Amount'];
                    var actual_budget = ['Actual Budget'];
                    for (rec = 0; rec < result.length; rec++) {
                        data.addColumn('string', result[rec].week);
                        actual_progress.push(result[rec].total_actual_progress);
                        total_actual_budget_list.push(result[rec].total_actual_budget);
                        actual_budget.push(result[rec].total_actual_budget_percent);
                    }
                    data.addRows([actual_progress, actual_budget, total_actual_budget_list]);
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.Table(document.getElementById('scurve_comparison_table'));
                    draw_table.draw(data, {
                        backgroundColor: '#f0eeee',
                        width: '100%',
                    });
                });
            });
        },

        // When Actual progress and Planned Budget
        ActualProPlannedBud: function(active_id) {
            var d = new Date();
            var merge_dict = new Model('project.project').call("merge_progress_budget", [
                [active_id]
            ]).then(function(result) {
                // for graph preparing
                var graph = self.google.charts.load('current', {
                    'packages': ['corechart']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', 'Weeks'); // Implicit domain label col.
                    data.addColumn('number', 'Actual Progress');
                    data.addColumn({
                        type: 'boolean',
                        role: 'scope'
                    }); // scope col.
                    data.addColumn('number', 'Planned Budget');
                    var rec;
                    for (rec = 0; rec < result.length; rec++) {
                        var dt = new Date(result[rec].week_end_date);
                        if (d <= dt) {
                            var check = false;
                        } else {
                            var check = true;
                        }
                        data.addRows([
                            [result[rec].week,
                                parseFloat(result[rec].total_actual_progress),
                                check,
                                parseFloat(result[rec].total_planned_budget_percent),
                            ]
                        ]);
                    }
                    var options = {
                        title: 'Project Actual Progress and Planned Budget Graph Report',
                        curveType: 'function',
                        series: {
                            0: {
                                color: '#e2431e'
                            }, // RED color
                            1: {
                                color: '#ff9900'
                            }, // Yellow color
                        },
                        backgroundColor: '#f0eeee',
                        legend: {
                            position: 'bottom'
                        }
                    };
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.LineChart(document.getElementById('scurve_comparison_chart'));
                    draw_table.draw(data, options);
                });

                // for table preparing
                var table = self.google.charts.load('current', {
                    'packages': ['table']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', '');
                    var rec;
                    var actual_progress = ['Actual Progress'];
                    var planned_budget = ['Planned Budget'];
                    var total_planned_budget_list = ["Total Planned Budget Amount"];
                    for (rec = 0; rec < result.length; rec++) {
                        data.addColumn('string', result[rec].week);
                        actual_progress.push(result[rec].total_actual_progress);
                        planned_budget.push(result[rec].total_planned_budget_percent);
                        total_planned_budget_list.push(result[rec].total_planned_budget);
                    }
                    data.addRows([actual_progress, planned_budget, total_planned_budget_list]);
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.Table(document.getElementById('scurve_comparison_table'));
                    draw_table.draw(data, {
                        backgroundColor: '#f0eeee',
                        width: '100%',
                    });
                });
            });
        },

        // When Planned Progress and Actual Budget
        PlannedProgressActualBudget: function(active_id) {
            var merge_dict = new Model('project.project').call("merge_progress_budget", [
                [active_id]
            ]).then(function(result) {
                // for graph preparing
                var graph = self.google.charts.load('current', {
                    'packages': ['corechart']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', 'Weeks'); // Implicit domain label col.
                    data.addColumn('number', 'Planned Progress');
                    data.addColumn('number', 'Actual Budget');
                    var rec;
                    for (rec = 0; rec < result.length; rec++) {
                        data.addRows([
                            [result[rec].week,
                                parseFloat(result[rec].total_planned_progress),
                                parseFloat(result[rec].total_actual_budget_percent)
                            ]
                        ]);
                    }
                    var options = {
                        title: 'Project Planned Progress and Actual Budget Graph Report',
                        curveType: 'function',
                        series: {
                            0: {
                                color: '#3366cc'
                            }, // blue color
                            1: {
                                color: '#109618'
                            }, // Green color
                        },
                        backgroundColor: '#f0eeee',
                        legend: {
                            position: 'bottom'
                        }
                    };
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.LineChart(document.getElementById('scurve_comparison_chart'));
                    draw_table.draw(data, options);
                });

                // for table preparing
                var table = self.google.charts.load('current', {
                    'packages': ['table']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', '');
                    var rec;
                    var planned_progress = ['Planned Progress'];
                    var actual_budget = ['Actual Budget'];
                    var total_actual_budget_list = ['Total Actual Budget Amount'];
                    for (rec = 0; rec < result.length; rec++) {
                        data.addColumn('string', result[rec].week);
                        planned_progress.push(result[rec].total_planned_progress);
                        total_actual_budget_list.push(result[rec].total_actual_budget);
                        actual_budget.push(result[rec].total_actual_budget_percent);
                    }
                    data.addRows([planned_progress, actual_budget, total_actual_budget_list]);
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.Table(document.getElementById('scurve_comparison_table'));
                    draw_table.draw(data, {
                        backgroundColor: '#f0eeee',
                        width: '100%',
                    });
                });
            });
        },

        // When Planned progress and Planned budget
        PlannedProgressBudget: function(active_id) {
            var merge_dict = new Model('project.project').call("merge_progress_budget", [
                [active_id]
            ]).then(function(result) {
                // for graph preparing
                var graph = self.google.charts.load('current', {
                    'packages': ['corechart']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', 'Weeks'); // Implicit domain label col.
                    data.addColumn('number', 'Planned Progress');
                    data.addColumn('number', 'Planned Budget');
                    var rec;
                    for (rec = 0; rec < result.length; rec++) {
                        data.addRows([
                            [result[rec].week,
                                parseFloat(result[rec].total_planned_progress),
                                parseFloat(result[rec].total_planned_budget_percent)
                            ]
                        ]);
                    }
                    var options = {
                        title: 'Project Planned Progress and Budget Graph Report',
                        curveType: 'function',
                        series: {
                            0: {
                                color: '#3366cc'
                            }, // blue color
                            1: {
                                color: '#ff9900'
                            }, // Yellow color
                        },
                        backgroundColor: '#f0eeee',
                        legend: {
                            position: 'bottom'
                        }
                    };
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.LineChart(document.getElementById('scurve_comparison_chart'));
                    draw_table.draw(data, options);
                });

                // for table preparing
                var table = self.google.charts.load('current', {
                    'packages': ['table']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', '');
                    var rec;
                    var planned_progress = ['Planned Progress'];
                    var planned_budget = ['Planned Budget'];
                    var total_planned_budget_list = ['Total Planned Budget Amount'];
                    for (rec = 0; rec < result.length; rec++) {
                        data.addColumn('string', result[rec].week);
                        planned_progress.push(result[rec].total_planned_progress);
                        planned_budget.push(result[rec].total_planned_budget_percent);
                        total_planned_budget_list.push(result[rec].total_planned_budget);
                    }
                    data.addRows([planned_progress, planned_budget, total_planned_budget_list]);
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.Table(document.getElementById('scurve_comparison_table'));
                    draw_table.draw(data, {
                        backgroundColor: '#f0eeee',
                        width: '100%',
                    });
                });
            });

        },

        // When both budget and Actual Progress.
        BothBudgetActualProgress: function(active_id) {
            var d = new Date();
            var merge_dict = new Model('project.project').call("merge_progress_budget", [
                [active_id]
            ]).then(function(result) {
                // for graph preparing
                var graph = self.google.charts.load('current', {
                    'packages': ['corechart']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', 'Weeks'); // Implicit domain label col.
                    data.addColumn('number', 'Actual Progress');
                    data.addColumn({
                        type: 'boolean',
                        role: 'scope'
                    }); // scope col.
                    data.addColumn('number', 'Planned Budget');
                    data.addColumn('number', 'Actual Budget');
                    var rec;
                    for (rec = 0; rec < result.length; rec++) {
                        var dt = new Date(result[rec].week_end_date);
                        if (d <= dt) {
                            var check = false;
                        } else {
                            var check = true;
                        }
                        data.addRows([
                            [result[rec].week,
                                parseFloat(result[rec].total_actual_progress),
                                check,
                                parseFloat(result[rec].total_planned_budget_percent),
                                parseFloat(result[rec].total_actual_budget_percent),
                            ]
                        ]);
                    }
                    var options = {
                        title: 'Project Planned Progress and Budget Graph Report',
                        curveType: 'function',
                        series: {
                            0: {
                                color: '#e2431e'
                            }, // REd color
                            1: {
                                color: '#ff9900'
                            }, // Yellow color
                            2: {
                                color: '#109618'
                            }, // Green color
                        },
                        backgroundColor: '#f0eeee',
                        legend: {
                            position: 'bottom'
                        }
                    };
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.LineChart(document.getElementById('scurve_comparison_chart'));
                    draw_table.draw(data, options);
                });

                // for table preparing
                var table = self.google.charts.load('current', {
                    'packages': ['table']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', '');
                    var rec;
                    var planned_progress = ['Actual Progress'];
                    var planned_budget = ['Planned Budget'];
                    var total_planned_budget_list = ['Total Planned Budget Amount'];
                    var actual_budget = ['Actual Budget'];
                    var total_actual_budget_list = ['Total Actual Budget Amount'];
                    for (rec = 0; rec < result.length; rec++) {
                        data.addColumn('string', result[rec].week);
                        planned_progress.push(result[rec].total_actual_progress);
                        planned_budget.push(result[rec].total_planned_budget_percent);
                        actual_budget.push(result[rec].total_actual_budget_percent);
                        total_planned_budget_list.push(result[rec].total_planned_budget);
                        total_actual_budget_list.push(result[rec].total_actual_budget);
                    }
                    data.addRows([planned_progress, planned_budget, total_planned_budget_list, actual_budget, total_actual_budget_list]);
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.Table(document.getElementById('scurve_comparison_table'));
                    draw_table.draw(data, {
                        backgroundColor: '#f0eeee',
                        width: '100%',
                    });
                });
            });
        },

        // When both budget and Planned Progress.
        BothBudgetPlannedProgress: function(active_id) {
            var merge_dict = new Model('project.project').call("merge_progress_budget", [
                [active_id]
            ]).then(function(result) {
                // for graph preparing
                var graph = self.google.charts.load('current', {
                    'packages': ['corechart']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', 'Weeks'); // Implicit domain label col.
                    data.addColumn('number', 'Planned Progress');
                    data.addColumn('number', 'Planned Budget');
                    data.addColumn('number', 'Actual Budget');
                    var rec;
                    for (rec = 0; rec < result.length; rec++) {
                        data.addRows([
                            [result[rec].week,
                                parseFloat(result[rec].total_planned_progress),
                                parseFloat(result[rec].total_planned_budget_percent),
                                parseFloat(result[rec].total_actual_budget_percent),
                            ]
                        ]);
                    }
                    var options = {
                        title: 'Project Planned Progress and Budget Graph Report',
                        curveType: 'function',
                        series: {
                            0: {
                                color: '#3366cc'
                            }, // Blue color
                            1: {
                                color: '#ff9900'
                            }, // Yellow color
                            2: {
                                color: '#109618'
                            }, // Green color
                        },
                        backgroundColor: '#f0eeee',
                        legend: {
                            position: 'bottom'
                        }
                    };
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.LineChart(document.getElementById('scurve_comparison_chart'));
                    draw_table.draw(data, options);
                });
                // for table preparing
                var table = self.google.charts.load('current', {
                    'packages': ['table']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', '');
                    var rec;
                    var planned_progress = ['Planned Progress'];
                    var planned_budget = ['Planned Budget'];
                    var total_planned_budget_list = ["Total Planned Budget Amount"];
                    var actual_budget = ['Actual Budget'];
                    var total_actual_budget_list = ["Total Actual Budget Amount"];
                    for (rec = 0; rec < result.length; rec++) {
                        data.addColumn('string', result[rec].week);
                        planned_progress.push(result[rec].total_planned_progress);
                        planned_budget.push(result[rec].total_planned_budget_percent);
                        total_planned_budget_list.push(result[rec].total_planned_budget);
                        actual_budget.push(result[rec].total_actual_budget_percent);
                        total_actual_budget_list.push(result[rec].total_actual_budget);
                    }
                    data.addRows([planned_progress, planned_budget, total_planned_budget_list, actual_budget, total_actual_budget_list]);
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.Table(document.getElementById('scurve_comparison_table'));
                    draw_table.draw(data, {
                        backgroundColor: '#f0eeee',
                        width: '100%',
                    });
                });
            });

        },

        // When Both Progress:checked and Planned Budget:checked.
        BothProgressPlannedBudget: function(active_id) {
            var d = new Date();
            var merge_dict = new Model('project.project').call("merge_progress_budget", [
                [active_id]
            ]).then(function(result) {
                // for graph preparing
                var graph = self.google.charts.load('current', {
                    'packages': ['corechart']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', 'Weeks'); // Implicit domain label col.
                    data.addColumn('number', 'Planned Progress');
                    data.addColumn('number', 'Actual Progress');
                    data.addColumn({
                        type: 'boolean',
                        role: 'scope'
                    }); // scope col.
                    data.addColumn('number', 'Planned Budget');
                    var rec;
                    for (rec = 0; rec < result.length; rec++) {
                        var dt = new Date(result[rec].week_end_date);
                        if (d <= dt) {
                            var check = false;
                        } else {
                            var check = true;
                        }
                        data.addRows([
                            [result[rec].week,
                                parseFloat(result[rec].total_planned_progress),
                                parseFloat(result[rec].total_actual_progress),
                                check,
                                parseFloat(result[rec].total_planned_budget_percent),
                            ]
                        ]);
                    }

                    var options = {
                        title: 'Project Progress and Planned Budget Graph Report',
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

                // for table preparing
                var table = self.google.charts.load('current', {
                    'packages': ['table']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', '');
                    var rec;
                    var planned_progress = ['Planned Progress'];
                    var actual_progress = ['Actual Progress'];
                    var planned_budget = ['Planned Budget'];
                    var total_planned_budget_list = ["Total Planned Budget Amount"];
                    for (rec = 0; rec < result.length; rec++) {
                        data.addColumn('string', result[rec].week);
                        planned_progress.push(result[rec].total_planned_progress);
                        actual_progress.push(result[rec].total_actual_progress);
                        planned_budget.push(result[rec].total_planned_budget_percent);
                        total_planned_budget_list.push(result[rec].total_planned_budget)
                    }
                    data.addRows([planned_progress, actual_progress, planned_budget, total_planned_budget_list]);
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

        // When Both Progress:checked and Actual Budget:checked.
        BothProgressActualBudget: function(active_id) {
            var d = new Date(); //Current date for checking Forecast or not.
            var merge_dict = new Model('project.project').call("merge_progress_budget", [
                [active_id]
            ]).then(function(result) {
                // for graph preparing
                var graph = self.google.charts.load('current', {
                    'packages': ['corechart']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', 'Weeks'); // Implicit domain label col.
                    data.addColumn('number', 'Planned Progress');
                    data.addColumn('number', 'Actual Progress');
                    data.addColumn({
                        type: 'boolean',
                        role: 'scope'
                    }); // scope col.
                    data.addColumn('number', 'Actual Budget');
                    var rec;
                    for (rec = 0; rec < result.length; rec++) {
                        var dt = new Date(result[rec].week_end_date);
                        if (d <= dt) {
                            var check = false;
                        } else {
                            var check = true;
                        }
                        data.addRows([
                            [result[rec].week,
                                parseFloat(result[rec].total_planned_progress),
                                parseFloat(result[rec].total_actual_progress),
                                check,
                                parseFloat(result[rec].total_actual_budget_percent),
                            ]
                        ]);
                    }
                    var options = {
                        title: 'Project Progress and Actual Budget Graph Report',
                        curveType: 'function',
                        series: {
                            0: {
                                color: '#3366cc'
                            }, // Blue color
                            1: {
                                color: '#e2431e'
                            }, // Red color
                            2: {
                                color: '#109618'
                            }, // Green color
                        },
                        backgroundColor: '#f0eeee',
                        legend: {
                            position: 'bottom'
                        }
                    };
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.LineChart(document.getElementById('scurve_comparison_chart'));
                    draw_table.draw(data, options);
                });

                // for table preparing
                var table = self.google.charts.load('current', {
                    'packages': ['table']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', '');
                    var rec;
                    var planned_progress = ['Planned Progress'];
                    var actual_progress = ['Actual Progress'];
                    var actual_budget = ['Actual Budget'];
                    var total_actual_budget_list = ['Total Actual Budget Amount'];
                    for (rec = 0; rec < result.length; rec++) {
                        data.addColumn('string', result[rec].week);
                        planned_progress.push(result[rec].total_planned_progress);
                        actual_progress.push(result[rec].total_actual_progress);
                        total_actual_budget_list.push(result[rec].total_actual_budget);
                        actual_budget.push(result[rec].total_actual_budget_percent);
                    }
                    data.addRows([planned_progress, actual_progress, actual_budget, total_actual_budget_list]);
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.Table(document.getElementById('scurve_comparison_table'));
                    draw_table.draw(data, {
                        backgroundColor: '#f0eeee',
                        width: '100%',
                    });
                });
            });
        },

        // When select all.
        SelectAll: function(active_id) {
            var d = new Date(); //Current date for checking Forecast or not.
            var merge_dict = new Model('project.project').call("merge_progress_budget", [
                [active_id]
            ]).then(function(result) {
                // for graph preparing
                var graph = self.google.charts.load('current', {
                    'packages': ['corechart']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', 'Weeks'); // Implicit domain label col.
                    data.addColumn('number', 'Planned Progress');
                    data.addColumn('number', 'Actual Progress');
                    data.addColumn({
                        type: 'boolean',
                        role: 'scope'
                    }); // scope col.
                    data.addColumn('number', 'Planned Budget');
                    data.addColumn('number', 'Actual Budget');
                    var rec;
                    for (rec = 0; rec < result.length; rec++) {
                        var dt = new Date(result[rec].week_end_date);
                        if (d <= dt) {
                            var check = false;
                        } else {
                            var check = true;
                        }
                        data.addRows([
                            [result[rec].week,
                                parseFloat(result[rec].total_planned_progress),
                                parseFloat(result[rec].total_actual_progress),
                                check,
                                parseFloat(result[rec].total_planned_budget_percent),
                                parseFloat(result[rec].total_actual_budget_percent),
                            ]
                        ]);
                    }
                    var options = {
                        title: 'Project Progress and Budget Graph Report',
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

                // for table preparing
                var table = self.google.charts.load('current', {
                    'packages': ['table']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', '');
                    var rec;
                    var planned_progress = ['Planned Progress'];
                    var actual_progress = ['Actual Progress'];
                    var planned_budget = ['Planned Budget'];
                    var total_planned_budget_list = ['Total Planned Budget Amount'];
                    var actual_budget = ['Actual Budget'];
                    var total_actual_budget_list = ['Total Actual Budget Amount'];
                    for (rec = 0; rec < result.length; rec++) {
                        data.addColumn('string', result[rec].week);
                        planned_progress.push(result[rec].total_planned_progress);
                        actual_progress.push(result[rec].total_actual_progress);
                        planned_budget.push(result[rec].total_planned_budget_percent);
                        actual_budget.push(result[rec].total_actual_budget_percent);
                        total_planned_budget_list.push(result[rec].total_planned_budget);
                        total_actual_budget_list.push(result[rec].total_actual_budget);
                    }
                    data.addRows([planned_progress, actual_progress, planned_budget, total_planned_budget_list, actual_budget, total_actual_budget_list]);
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.Table(document.getElementById('scurve_comparison_table'));
                    draw_table.draw(data, {
                        backgroundColor: '#f0eeee',
                        width: '100%',
                    });
                });
            });
        },

        // when select only Planned budget.
        SelectPlannedBudget: function(active_id) {
            // for graph
            var val = new Model('project.project').call("get_project_budget_data", [
                [parseInt(active_id)]
            ]).then(function(result) {
                var graph = self.google.charts.load('current', {
                    'packages': ['corechart']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', 'Weeks'); // Implicit domain label col.
                    data.addColumn('number', 'Planned Budget'); // Implicit series 1 data col.
                    var rec;
                    for (rec = 0; rec < result.length; rec++) {
                        data.addRows([
                            [result[rec].week, parseFloat(result[rec].total_planned_budget_percent)]
                        ]);
                    }
                    var options = {
                        title: 'Project Planned Budget Graph Report',
                        series: {
                            0: {
                                color: '#ff9900'
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
                // for table
                var table = self.google.charts.load('current', {
                    'packages': ['table']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', '');
                    var rec;
                    var planned_progress = ['Planned Budget'];
                    var total_planned_budget_var = ['Total Planned Budget Amount'];
                    for (rec = 0; rec < result.length; rec++) {
                        data.addColumn('string', result[rec].week);
                        planned_progress.push(result[rec].total_planned_budget_percent);
                        total_planned_budget_var.push(result[rec].total_planned_budget);
                    }
                    data.addRows([planned_progress, total_planned_budget_var]);
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.Table(document.getElementById('scurve_comparison_table'));
                    draw_table.draw(data, {
                        backgroundColor: '#f0eeee',
                        width: '100%',
                    });
                });
            });
        },

        // when select only Actual budget.
        SelectActualBudget: function(active_id) {
            var val = new Model('project.project').call("get_project_budget_data", [
                [parseInt(active_id)]
            ]).then(function(result) {
                // For graph
                var graph = self.google.charts.load('current', {
                    'packages': ['corechart']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', 'Weeks'); // Implicit domain label col.
                    data.addColumn('number', 'Actual Budget');
                    var rec;
                    for (rec = 0; rec < result.length; rec++) {
                        data.addRows([
                            [result[rec].week, parseFloat(result[rec].total_actual_budget_percent)]
                        ]);
                    }
                    var options = {
                        title: 'Project Actual Budget Graph Report',
                        curveType: 'function',
                        backgroundColor: '#f0eeee',
                        series: {
                            0: {
                                color: '#109618'
                            }
                        },
                        legend: {
                            position: 'bottom'
                        }
                    };
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.LineChart(document.getElementById('scurve_comparison_chart'));
                    draw_table.draw(data, options);
                });
                // for table
                var table = self.google.charts.load('current', {
                    'packages': ['table']
                }).then(function() {
                    var data = new self.google.visualization.DataTable();
                    data.addColumn('string', '');
                    var rec;
                    var actual_budget_list = ['Actual Budget'];
                    var total_actual_budget_list = ['Total Actual Budget Amount'];
                    for (rec = 0; rec < result.length; rec++) {
                        data.addColumn('string', result[rec].week);
                        actual_budget_list.push(result[rec].total_actual_budget_percent);
                        total_actual_budget_list.push(result[rec].total_actual_budget);
                    }
                    data.addRows([actual_budget_list, total_actual_budget_list]);
                    var load = self.google.charts.setOnLoadCallback(data);
                    var draw_table = new google.visualization.Table(document.getElementById('scurve_comparison_table'));
                    draw_table.draw(data, {
                        backgroundColor: '#f0eeee',
                        width: '100%',
                    });
                });
            });
        },

        // click event for checkboxes.
        onClickPlannedActual: function(event) {
            var active = this.dataset.context.active_id;
            // When all are True
            if ($("#first_check:checked,#second_check:checked,#planned_budget_check:checked,#actual_budget_check:checked").length == 4) {
                return this.SelectAll(active);
            }
            // When any three are true
            if ($("#first_check:checked,#second_check:checked,#planned_budget_check:checked,#actual_budget_check:checked").length == 3) {
                // WHEN first_check/Planned_Progress & second_check/Actual_Progress & planned_budget_check is True
                if (($("#first_check").prop("checked") === true) &&
                    ($("#second_check").prop("checked") === true) &&
                    ($('#planned_budget_check').prop("checked") === true)) {
                    return this.BothProgressPlannedBudget(active);
                }
                // WHEN first_check/Planned_Progress & second_check/Actual_Progress & actual_budget_check is True
                if (($("#first_check").prop("checked") === true) &&
                    ($("#second_check").prop("checked") === true) &&
                    ($('#actual_budget_check').prop("checked") === true)) {
                    return this.BothProgressActualBudget(active);
                }
                // WHEN first_check & planned_budget_check & actual_budget_check is True
                if (($("#first_check").prop("checked") === true) &&
                    ($("#planned_budget_check").prop("checked") === true) &&
                    ($('#actual_budget_check').prop("checked") === true)) {
                    return this.BothBudgetPlannedProgress(active);
                }
                // WHEN second_check & planned_budget_check & actual_budget_check is True
                if (($("#second_check").prop("checked") === true) &&
                    ($("#planned_budget_check").prop("checked") === true) &&
                    ($('#actual_budget_check').prop("checked") === true)) {
                    return this.BothBudgetActualProgress(active);
                }
            }
            // When any two are True
            if ($("#first_check:checked,#second_check:checked,#planned_budget_check:checked,#actual_budget_check:checked").length == 2) {
                // Planned Progress: checked and Actual Progress: checked
                if (($("#first_check").prop("checked") === true) &&
                    ($("#second_check").prop("checked") === true)) {
                    return this.SelectPlannedActualBoth(active);
                }
                // Planned Progress: checked and Planned Budget: checked
                if (($("#first_check").prop("checked") === true) &&
                    ($("#planned_budget_check").prop("checked") === true)) {
                    return this.PlannedProgressBudget(active);
                }
                // Planned Progress: checked and Actual Budget: checked
                if (($("#first_check").prop("checked") === true) &&
                    ($("#actual_budget_check").prop("checked") === true)) {
                    return this.PlannedProgressActualBudget(active);
                }
                // Actual Progress: checked and Planned Budget: checked
                if (($("#second_check").prop("checked") === true) &&
                    ($("#planned_budget_check").prop("checked") === true)) {
                    return this.ActualProPlannedBud(active);
                }
                // Actual Progress: checked and Actual Budget: checked
                if (($("#second_check").prop("checked") === true) &&
                    ($("#actual_budget_check").prop("checked") === true)) {
                    return this.ActualProgressBudget(active);
                }
                // Planned Budget: checked and Actual Budget: checked
                if (($("#planned_budget_check").prop("checked") === true) &&
                    ($("#actual_budget_check").prop("checked") === true)) {
                    return this.PlannedActualBudget(active);
                }
            }
            // When any one is True
            if ($("#first_check:checked,#second_check:checked,#planned_budget_check:checked,#actual_budget_check:checked").length == 1) {
                if ($("#first_check").prop("checked") === true) {
                    return this.SelectPlannedProgress(active);
                }
                if ($("#second_check").prop("checked") === true) {
                    return this.SelectActualProgress(active);
                }
                if ($('#planned_budget_check').prop("checked") === true) {
                    return this.SelectPlannedBudget(active);
                }
                if ($('#actual_budget_check').prop("checked") === true) {
                    return this.SelectActualBudget(active);
                }
            }
            // When all are False
            if ($("#first_check:checked,#second_check:checked,#planned_budget_check:checked,#actual_budget_check:checked").length === 0) {
                alert("Please select at least one!");
                $(event.target).context.checked = true;
            }
        },

        willStart: function() {
            this.SelectAll(this.dataset.context.active_id);
            return this._super();
        },
    });
});