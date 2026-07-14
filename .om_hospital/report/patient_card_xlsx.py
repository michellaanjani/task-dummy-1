# -*- coding: utf-8 -*-
from odoo import models
import base64
from PIL import Image
import io

class PatientCardXlsx(models.AbstractModel):
    _name = 'report.om_hospital.report_patient_id_card_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):
        sheet = workbook.add_worksheet('Patient ID Card')
        bold = workbook.add_format({'bold': True})
        format_1 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'yellow'}) 
        row = 3
        col = 3
        sheet.set_column('D:D', 12)
        sheet.set_column('E:E', 13)
        for obj in patients:
            row +=1
            sheet.merge_range(row, col, row, col+1, 'ID Card', format_1)

            row+=1
            if obj.image:
                # Resize dulu
                img = Image.open(io.BytesIO(base64.b64decode(obj.image)))
                img.thumbnail((100, 120))  # ⭐ Resize ke max 100×120

                # Save ke BytesIO
                output = io.BytesIO()
                img.save(output, format='PNG')
                output.seek(0)
                
                sheet.insert_image(row, col, 'patient_image.png', {'image_data': output, 'x_scale': 1, 'y_scale': 1})
                row +=6

            sheet.write(row, col, "Name: ", bold)
            sheet.write(row, col+1, obj.name)
            row +=1
            sheet.write(row, col, "Age: ", bold)
            sheet.write(row, col+1, obj.age)
            row +=1
            sheet.write(row, col, "ID Reference: ", bold)
            sheet.write(row, col+1, obj.reference)

            row +=2
            sheet.merge_range(row, col, row+1, col+1, '', format_1)
            row +=2
