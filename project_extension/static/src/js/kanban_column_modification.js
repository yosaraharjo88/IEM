odoo.define('project_extension.Column', function (require) {
"use strict";

var core = require('web.core');
var web_kanban = require('web_kanban.Column');
var Model = require('web.DataModel');
var QWeb = core.qweb;
var quick_create = require('web_kanban.quick_create');
var RecordQuickCreate = quick_create.RecordQuickCreate;


web_kanban.include({
    update_column: function () {
        this._super();
        var cal = 0.0;
        if(this.relation == "project.task.type" && !this.folded){
            var self = this;
            for (var rec in self.data_records){
                var data = self.data_records[rec];
                var pg = data['planned_progress'];
                var pc = data['progress_completion'];
                var grand =  (pg*((pc)/100));
                cal = cal + grand;
            }

            new Model(self.dataset.model)
            .call("search_read", [[['id','=',self.dataset.ids[0]]], ['project_id']])
            .then(function(project){
                if (project[0]){
                    new Model('project.stage.project')
                    .call("search_read", [[['type_id', '=', self.id],['project_id','=',project[0].project_id[0]]], ['stage_weightage','stage_completion']])
                    .then(function(stage){
                        self.$('#task_progressbar').html(QWeb.render('KanbanView.task_progressbar', {}));
                        if(stage.length > 0){
                            var weight = stage[0].stage_weightage;
                            if (cal % 1 != 0){
                                var per = cal.toFixed(2);
                            }
                            else{var per = cal}
                            self.$('#task_progressbar').find('.o_progressbar_values').html(weight + '%');
                            self.$('#task_progressbar').find('.o_progressbar_complete').css('width', per + '%');
                            self.$('#task_progressbar').find('.o_progressbar_value').html(per + '%');
                        }
                    });
                }
            });
        }
    },
    add_quick_create: function () {
        if (this.quick_create_widget) {
            return;
        }
        var self = this;
        var width = this.records.length ? this.records[0].$el.innerWidth() : this.$el.width() - 8;
        this.quick_create_widget = new RecordQuickCreate(this, width);
        if(this.relation == "project.task.type" && !this.folded){
            this.quick_create_widget.insertAfter(this.$('#task_progressbar'));
        }else{
            this.quick_create_widget.insertAfter(this.$header);
        }
        this.quick_create_widget.$el.focusout(function () {
            var hasFocus = (self.quick_create_widget.$(':focus').length > 0);
            if (! hasFocus && self.quick_create_widget) {
                self.cancel_quick_create();
            }
        });

    },

})

});