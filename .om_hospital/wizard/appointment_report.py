# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AppointmentReportWizard(models.TransientModel):
    _name = "appointment.report.wizard"
    _description = "Print Appointment Wizard"

    patient_id = fields.Many2one('hospital.patient', string="Patient")
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    def action_print_report(self):
        print(self.read()[0])
        domain = []
        if self.patient_id:
            domain.append(('patient_id', '=', self.patient_id.id))
        
        if self.date_from:
            domain.append(('date_appointment', '>=', self.date_from))

        if self.date_to:
            domain.append(('date_appointment', '<=', self.date_to))
        
        print("domain",domain)
        
        #Method 1 -> Bisa pake search_read
        # appointments = self.env['hospital.appointment'].search_read(domain)
        # data = {
        #     'form': self.read()[0],
        #     'appointments': appointments,
        # }

        #Method 2 -> Bisa pake search
        appointments = self.env['hospital.appointment'].search(domain)
        appointment_list =[]
        for rec in appointments:
            vals = {
                'reference': rec.reference,
                'note': rec.note,
                'age': rec.age,
            }
            appointment_list.append(vals)

        data = {
            'form': self.read()[0],
            'appointments': appointment_list,
        }
        return self.env.ref('om_hospital.report_patient_appointment').report_action(self, data=data)
    
    def action_print_excel_report(self):
        #ini bakal ngirim semua data/field patient
        # data = {
        #     'form': self.read()[0],
        # }


        #Ini cuman kirim data yang diperlukan aja       
        domain = []
        if self.patient_id:
            domain.append(('patient_id', '=', self.patient_id.id))
        
        if self.date_from:
            domain.append(('date_appointment', '>=', self.date_from))

        if self.date_to:
            domain.append(('date_appointment', '<=', self.date_to))
        
        print("domain",domain)

        appointments = self.env['hospital.appointment'].search_read(domain)
        data={
            'appointments': appointments,
            'form': self.read()[0]
        }
        return self.env.ref('om_hospital.report_patient_appointment_xlsx').report_action(self, data=data)