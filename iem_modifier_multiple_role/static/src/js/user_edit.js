odoo.define('apsn_hide_import.hide_import', function (require) {
"use strict";

var Model = require('web.DataModel');
var FormView = require('web.FormView');
var ListView = require('web.ListView');
var core = require('web.core');
var QWeb = core.qweb;
var ListView = require('web.View');

	FormView.include({
	    load_record: function (record) {
	        var self = this;
	        self._super.apply(self, arguments);
	
	        if (self.model == 'project.project') {
	        	var record_id = self.datarecord.id
	        	new Model('project.project').call('check_action', [record_id]).then(function (check_action) {
                    if (check_action) {
                    	self.$buttons.find('.o_form_button_edit').removeClass('hidden_btnedit_important');
                    }else{
                    	self.$buttons.find('.o_form_button_edit').addClass('hidden_btnedit_important');
                    }
                });
	        }
	        if (self.model == 'project.task') {
	        	var record_id = self.datarecord.id
	        	new Model('project.task').call('check_action', [record_id]).then(function (check_action) {
                    if (check_action) {
                    	self.$buttons.find('.o_form_button_edit').removeClass('hidden_btnedit_important');
                    }else{
                    	self.$buttons.find('.o_form_button_edit').addClass('hidden_btnedit_important');
                    }
                });
	        }
	    },
	});

});