from odoo import models
import io
import base64

class PatientReportXlsx(models.AbstractModel):
    _name = 'report.om_hospital.report_patient_template_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, patients):

        # to print the details of each patient in different sheet:

        # for obj in patients:                         # looping in all records i will select
        #     print('patients', patients)              # patients hospital.patient(7, 27, 32) all records i selected
        #     report_name = obj.name
        #
        #     # One sheet by partner
        #     sheet = workbook.add_worksheet(report_name[:31])      # we can name each sheet any thing (report_name[:31]) or ("...")
        #     bold = workbook.add_format({'bold': True})
        #
        #     sheet.write(0, 0, obj.name, bold)                    # write (row, col, field, formating)
        #     sheet.write(0, 1, obj.age, bold)


        # to print all patients details in one sheet:

        sheet = workbook.add_worksheet('Patient Details')
        bold = workbook.add_format({'bold': True})
        format_1 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'yellow'})

        row = 0
        col = 0

        sheet.set_column('A:C', 20)               # to define the size of columns from A to C (we can set B:B) for 1 column
        sheet.merge_range(row, col, row, col+1, 'Patients', format_1)    # to merge row & col with other row & col

        row += 1
        sheet.write(row, col, 'Name', bold)
        sheet.write(row, col+1, 'Age', bold)

        for obj in patients:
            row += 1
            sheet.write(row, col, obj.name)
            sheet.write(row, col + 1, obj.age)

            # print patients imgs:

            if obj.image:
                product_image = io.BytesIO(base64.b64decode(obj.image))
                sheet.insert_image(row, col + 2, 'image.png', {'image_data': product_image, 'x_scale': 0.5, 'y_scale': 0.5})
                row += 5




