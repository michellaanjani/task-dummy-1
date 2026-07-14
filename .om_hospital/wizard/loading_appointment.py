# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import time

class LoadingAppointmentWizard(models.TransientModel):
    _name = "loading.appointment.wizard"
    _description = "Loading Appointment Wizard"
    
    def action_loading_appointment(self):
        appointments = self.env['hospital.appointment'].search([])
        # (https://apps.odoo.com/apps/modules/14.0/web_progress)
        for app in appointments.with_progress(msg='Confirming Appointments'):
            time.sleep(0.3)
            app.action_confirm()
            
            time.sleep(0.3)
            app.action_done()
            
            time.sleep(0.3)
            app.action_cancel()
            
            time.sleep(0.3)
            app.action_confirm()
            
