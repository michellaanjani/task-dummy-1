# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AllPatientReport(models.AbstractModel):
    _name = "report.om_hospital.report_patient_list" #syntax -> report.module_name.template_name
    _description = "Patient Report"

    @api.model
    def _get_report_values(self, data=None):
        #function ini jalan ketika kita klik button print
        print("data:", data)

        domain = []
        gender = data.get('form').get('gender') 
        age = data.get('form').get('age') 

        if gender:
            domain.append(('gender', '=', gender))

        if age !=0:
            domain.append(('age', '=', age))
        docs = self.env['hospital.patient'].search(domain) # Ambil data pasien berdasarkan ID
        return {
            'docs': docs,
            'email': 'exampleSSS@gmail.com'
        }
        
    # class PatientDetailsReport(models.AbstractModel):
    # _name = "report.om_hospital.report_patient_detail" #syntax -> report.module_name.template_name
    # _description = "Patient Details Report"

    # @api.model
    # def _get_report_values(self, docids, data=None):
    #     #function ini jalan ketika kita klik button print
    #     print(docids)
    #     print(data)
    #     docs = self.env['hospital.patient'].browse(docids) # Ambil data pasien berdasarkan ID
    #     return {
    #         'docs': docs,
    #     }