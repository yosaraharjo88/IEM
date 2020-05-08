from odoo import models, fields, api,_
from dateutil.relativedelta import relativedelta
import datetime 
from odoo.exceptions import UserError

class TimeSheetLeaveLine(models.Model):
    _name = "time.sheet.leave.line"
    
    date = fields.Date('Date')
    description = fields.Char('Description')
    leave_hours = fields.Float("Hours")
    sheet_id = fields.Many2one('hr_timesheet_sheet.sheet', string ="Sheet")

class HrTimesheetSheet(models.Model):
    _inherit = 'hr_timesheet_sheet.sheet'
    
    leave_ids = fields.One2many('time.sheet.leave.line', 'sheet_id', string='Leave lines')
    
    @api.multi
    @api.depends('date_from')
    def _get_date_to(self):
        for rec in self:
            if rec.date_from:
                end_date = datetime.datetime.strptime(rec.date_from,'%Y-%m-%d') + datetime.timedelta(days=6)
                rec.date_to = end_date.date()
    
    date_to = fields.Date(string='Date To', required=True,
        index=True, compute="_get_date_to" ,store=True)
   
    @api.multi
    @api.onchange('date_from')
    def onchange_date_from(self):
        for rec in self:
            if rec.date_from:
                end_date = datetime.datetime.strptime(rec.date_from,'%Y-%m-%d') + datetime.timedelta(days=6)
                rec.date_to = end_date.date()
   
    

    @api.multi
    def action_submit(self):
        res = super(HrTimesheetSheet, self).action_submit()
        AccountLine = self.env['account.analytic.line'].search([('sheet_id','=',self.id)])
        LeaveLine = self.env['time.sheet.leave.line'].search([('sheet_id','=',self.id)])

        Values = self.env['ir.values'].sudo() or self.env['ir.values']
        hours = Values.get_default('time.sheet.setting', 'hours')
        mon_hours = Values.get_default('time.sheet.setting', 'monday')
        tue_hours = Values.get_default('time.sheet.setting', 'tuesday')
        wen_hours = Values.get_default('time.sheet.setting', 'wednesday')
        thu_hours = Values.get_default('time.sheet.setting', 'thursday')
        fri_hours = Values.get_default('time.sheet.setting', 'friday')
        sat_hours = Values.get_default('time.sheet.setting', 'saturday')
        sun_hours = Values.get_default('time.sheet.setting', 'sunday')
        mon = Values.get_default('time.sheet.setting', 'mon')
        tue = Values.get_default('time.sheet.setting', 'tue')
        wen = Values.get_default('time.sheet.setting', 'wed')
        thu = Values.get_default('time.sheet.setting', 'thu')
        fri = Values.get_default('time.sheet.setting', 'fri')
        sat = Values.get_default('time.sheet.setting', 'sat')
        sun = Values.get_default('time.sheet.setting', 'sun')
        show = Values.get_default('time.sheet.setting', 'show')
        total_hours = 0.00
        if show == True:
            hours_m = 0.00
            hours_t = 0.00
            hours_w = 0.00
            hours_th = 0.00
            hours_f = 0.00
            hours_s = 0.00
            hours_su = 0.00
            total_hours1 = 0.00
            values = []
            msg = ""
            for line in AccountLine:
                
                day = datetime.datetime.strptime(line.date ,'%Y-%m-%d') 
                days = datetime.date.strftime(day,'%A')      
                if str(days) == str(mon):
                    hours_m += line.unit_amount                    
                   
                if str(days) == str(tue):
                    hours_t += line.unit_amount
                    
                if str(days) == str(wen):
                    hours_w += line.unit_amount
                    
                if str(days) == str(thu):
                    hours_th += line.unit_amount
                    
                
                if str(days) == str(fri):
                    hours_f += line.unit_amount
                    
                        
                if str(days) == str(sat):
                    hours_s += line.unit_amount
                    
             
                if str(days) == str(sun):
                    hours_su += line.unit_amount
                                        
                total_hours1 += line.unit_amount
            for lev_line in LeaveLine:
               
                lev_day = datetime.datetime.strptime(lev_line.date ,'%Y-%m-%d') 
                lev_days = datetime.date.strftime(lev_day,'%A')      
                if str(lev_days) == str(mon):
                    hours_m += lev_line.leave_hours
                  
                if str(lev_days) == str(tue):
                    hours_t += lev_line.leave_hours
                  
                if str(lev_days) == str(wen):
                    hours_w += lev_line.leave_hours
                  
                if str(lev_days) == str(thu):
                    hours_th += lev_line.leave_hours
                    
                
                if str(lev_days) == str(fri):
                    hours_f += lev_line.leave_hours
                    
                        
                if str(lev_days) == str(sat):
                    hours_s += lev_line.leave_hours
                    
             
                if str(lev_days) == str(sun):
                    hours_su += lev_line.leave_hours
                      
            if hours_m != 0.00 and hours_m < mon_hours:
                raise UserError(_('You have not reached timesheet minimum hours (%s).The days that minimal hours not reached is: %s (%s)') % (hours, mon, mon_hours))
            else:
                if hours_m != mon_hours and hours_m < mon_hours:
                    vals = {'Monday' : mon_hours,
                            }
                    values.append(vals)
                
            if hours_t != 0.00 and hours_t < tue_hours:
                raise UserError(_('You have not reached timesheet minimum hours (%s).The days that minimal hours not reached is: %s (%s)') % (hours, tue, tue_hours))
            else:
                if hours_t != tue_hours and hours_t < tue_hours:
                    vals = {'Tuesday' : tue_hours,
                            }
                    values.append(vals)
                    
            if hours_w != 0.00 and hours_w < wen_hours:
                raise UserError(_('You have not reached timesheet minimum hours (%s).The days that minimal hours not reached is: %s (%s)') % (hours, wen, wen_hours))
            else:
                if hours_w != wen_hours and hours_w < wen_hours:
                    vals = {'Wednesday' : wen_hours,
                            }
                    values.append(vals)    
             
            if hours_th != 0.00 and hours_th < thu_hours:
                raise UserError(_('You have not reached timesheet minimum hours (%s).The days that minimal hours not reached is: %s (%s)') % (hours, thu, thu_hours))
            else:
                if hours_th != thu_hours and hours_th < thu_hours:
                    vals = {'Thursday' : thu_hours,
                            }
                    values.append(vals)   
             
            if hours_f != 0.00 and hours_f < fri_hours:
                raise UserError(_('You have not reached timesheet minimum hours (%s).The days that minimal hours not reached is: %s (%s)') % (hours, fri, fri_hours))
            else:
                if hours_f != fri_hours and hours_f < fri_hours:
                    vals = {'Friday' : fri_hours,
                            }
                    values.append(vals)
             
            if hours_s != 0.00 and hours_s < sat_hours:
                raise UserError(_('You have not reached timesheet minimum hours (%s).The days that minimal hours not reached is: %s (%s)') % (hours, sat, sat_hours))
            else:
                if hours_s != sat_hours and hours_s < sat_hours:
                    vals = {'Saturday' : sat_hours,
                            }
                    values.append(vals)   
             
            if hours_su != 0.00 and hours_su < sun_hours:
                raise UserError(_('You have not reached timesheet minimum hours (%s).The days that minimal hours not reached is: %s (%s)') % (hours, sun, sun_hours))
            else:
                if hours_su != sun_hours and hours_su < sun_hours:
                    vals = {'Sunday' : sun_hours,
                            }
                    values.append(vals)
            
            for d in values:
                for key,value in d.iteritems():
                    m = key + " " + "(" + str(value) + ")" + ", "
                    msg += m   
                    
            if (hours_m != mon_hours and hours_m < mon_hours and hours != 0) or (hours_t != tue_hours and hours_t < tue_hours and hours) or (hours_w != wen_hours and hours_w < wen_hours and hours) or \
                (hours_th != thu_hours and hours_th < thu_hours and hours != 0) or (hours_f != fri_hours and hours_f < fri_hours and hours != 0) or \
                (hours_s != sat_hours and hours_s < sat_hours and hours != 0) or (hours_su != sun_hours and hours_su < sun_hours and hours != 0):
                raise UserError(_('You have not reached timesheet minimum hours (%s).The days that minimal hours not reached is: %s') %(hours, msg)) 
            
        else:
            for line in AccountLine:
                total_hours += line.unit_amount 
                
            if total_hours < hours and hours != 0:
                raise UserError(_('You have not reached timesheet minimum hours (%s)') % str(hours))
        return res  

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    name = fields.Char('Description', required=False)
    date = fields.Date('Date', required=True, index=True, default=lambda self:self.env.context.get('timesheet_date_from'))

    @api.onchange("date")
    def onchange_check_date_waring(self):
        for line in self:
            if line.date:
                if line.date < self.env.context.get('timesheet_date_from') or line.date > self.env.context.get('timesheet_date_to'):
                    raise UserError(_('Please Choose Date Between Timesheet Period Range'))

class TimeSheetSetting(models.TransientModel):
    _name = "time.sheet.setting"
    _inherit = 'res.config.settings'
    
    hours = fields.Float("Timesheet Minimum Hours", store=True)
    monday = fields.Float("Monday")
    tuesday = fields.Float("Tuesday")
    wednesday = fields.Float("Wednesday")
    thursday = fields.Float("Thursday")
    friday = fields.Float("Friday")
    saturday = fields.Float("Saturday")
    sunday = fields.Float("Sunday")
    mon = fields.Char("Monday")
    tue = fields.Char("Tuesday")
    wed = fields.Char("Wednesday")
    thu = fields.Char("Thursday")
    fri = fields.Char("Friday")
    sat = fields.Char("Saturday")
    sun = fields.Char("Sunday")
    show = fields.Boolean("Show")
    hide = fields.Boolean("Hide")
    
    @api.multi
    def action_show(self):
        for rec in self:
            if rec:
                rec.show = True
                rec.hide = False
                
    @api.multi 
    def action_hide(self):
        for rec in self:
            if rec:
                rec.hide = True
                rec.show = False
                rec.monday = 0.00  
                rec.mon = ""
                rec.tuesday = 0.00  
                rec.tue = ""
                rec.wednesday = 0.00  
                rec.wed = ""
                rec.thursday = 0.00  
                rec.thu = ""
                rec.friday = 0.00  
                rec.fri = ""
                rec.saturday = 0.00  
                rec.sat = ""
                rec.sunday = 0.00  
                rec.sun = ""
                rec.hours = 0.00
    
    @api.onchange('monday','tuesday','wednesday','thursday','friday','saturday','sunday')
    def onchange_show_fields(self):
        if self.monday or self.tuesday or self.wednesday or self.thursday or self.friday or self.saturday or self.sunday:
            self.hours = self.monday + self.tuesday + self.wednesday + self.thursday + self.friday + self.saturday + self.sunday

    @api.onchange('monday')
    def _onchange_monday(self):
        if self.monday:
            self.mon = "Monday"
    
    @api.onchange('tuesday')
    def _onchange_tuesday(self):
        if self.tuesday:
            self.tue = "Tuesday"
    
    @api.onchange('wednesday')
    def _onchange_wednesday(self):
        if self.wednesday:
            self.wed = "Wednesday"
            
    @api.onchange('thursday')
    def _onchange_thursday(self):
        if self.thursday:
            self.thu = "Thursday"
            
    @api.onchange('friday')
    def _onchange_friday(self):
        if self.friday:
            self.fri = "Friday"  
            
    @api.onchange('saturday')
    def _onchange_saturday(self):
        if self.saturday:
            self.sat = "Saturday"
            
    @api.onchange('sunday')
    def _onchange_sunday(self):
        if self.sunday:
            self.sun = "Sunday"

    @api.multi
    def set_default_exceeded(self):
        check = self.env.user.has_group('base.group_system')
        Values = check and self.env['ir.values'].sudo() or self.env['ir.values']
        for config in self:
            Values.set_default('time.sheet.setting', 'hours', config.hours)
    

    @api.multi
    def set_days(self):
        check = self.env.user.has_group('base.group_system')
        Values = check and self.env['ir.values'].sudo() or self.env['ir.values']
        for config in self:
            Values.set_default('time.sheet.setting', 'monday', config.monday)
            Values.set_default('time.sheet.setting', 'tuesday', config.tuesday)
            Values.set_default('time.sheet.setting', 'wednesday', config.wednesday)
            Values.set_default('time.sheet.setting', 'thursday', config.thursday)
            Values.set_default('time.sheet.setting', 'friday', config.friday)
            Values.set_default('time.sheet.setting', 'saturday', config.saturday)
            Values.set_default('time.sheet.setting', 'sunday', config.sunday)
            
            Values.set_default('time.sheet.setting', 'mon', config.mon)
            Values.set_default('time.sheet.setting', 'tue', config.tue)
            Values.set_default('time.sheet.setting', 'wed', config.wed)
            Values.set_default('time.sheet.setting', 'thu', config.thu)
            Values.set_default('time.sheet.setting', 'fri', config.fri)
            Values.set_default('time.sheet.setting', 'sat', config.sat)
            Values.set_default('time.sheet.setting', 'sun', config.sun)
            Values.set_default('time.sheet.setting', 'show', config.show)
            Values.set_default('time.sheet.setting', 'hide', config.hide)

    