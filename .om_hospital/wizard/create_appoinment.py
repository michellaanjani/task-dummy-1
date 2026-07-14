 # -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import time

class CreateAppointmentWizard(models.TransientModel):
    _name = "create.appointment.wizard"
    _description = "Create Appointment Wizard"

    @api.model
    def default_get(self, fields):
        print("Default Get Context: ", self._context)
        print("Default Get Fields: ", fields)
        print("Self: ", self)
        result = super(CreateAppointmentWizard, self).default_get(fields)
        print(self._context)
        if self._context.get('active_id'):
            result['patient_id'] = self._context.get('active_id')
        return result
    
    date_appointment = fields.Date(string='Date', required=True)
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)
       
    def action_create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            'date_appointment': self.date_appointment,
            'doctor_id': self.doctor_id.id,
        }
        appointment_rec = self.env['hospital.appointment'].create(vals)
        print("Appointment:", appointment_rec)
        print("Appointment ID: ", appointment_rec.id)
        return {
				    'name': _('Appointment'),  # Nama tampilan yang muncul di header
				    'type': 'ir.actions.act_window',  # Untuk membuka tampilan baru
				    'view_mode': 'form',  # Mode tampilan (bisa 'tree', 'form', 'kanban', dll.)
				    'res_model': 'hospital.appointment',  # Model yang akan ditampilkan
				    'res_id': appointment_rec.id,  # ID dari record yang baru dibuat
				    'target': 'current',  # Membuka di jendela saat ini (bisa 'new' untuk pop-up)
				     #target menentukan dimana tampilan baru akan dibuka.
		}
       
   