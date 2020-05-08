odoo.define('project_extension.kanban_button', function(require){
    "use strict";

    var core = require('web.core');
    var KanbanView = require('web_kanban.KanbanView');
    var Model = require('web.DataModel');
    
    var qweb = core.qweb;
    var _lt = core._lt;
    var _t = core._t;

    KanbanView.include({
        render_buttons: function($node){
            this._super.apply(this, arguments); //This is for super call
            var self = this;
            var res = '';
            if(this.model=="project.task" && self.search_context.active_id && this.$buttons){
                this.$buttons.on('click', 'button.o_project_details', function () {
                    var domain = [];
                    var context ={};
                    if (self.search_context.active_id){
                        domain = [['project_id', '=', self.search_context.active_id]]
                        context.default_project_id = self.search_context.active_id;
                    }
                    if(self.search_context.active_model){
                        new Model('project.project')
                        .call("search_read", [[['id','=',self.search_context.active_id]], ['id']])
                        .then(function(project){
                            if (project.length != 0){
                                res = project[0].id;
                            }
                            self.do_action({
                                type: 'ir.actions.act_window',
                                name: "Project Details",
                                res_model: 'project.project',
                                domain: domain,
                                context:context,
                                res_id: res,
                                views: [[false, 'form']],
                                target: 'current'
                            });
                        });
                    }
                });
            }
        },
    });
});