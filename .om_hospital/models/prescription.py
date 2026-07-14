from odoo import models, fields, api, _

class AppointmentPrescriptionLines(models.Model):
        _name = "appointment.prescription.lines"
        _description = "Appointment Prescription Lines"

        name = fields.Char(string='Name', required=True)
        qty = fields.Integer(string='Quantity', required=True)
        appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
       