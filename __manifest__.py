# -*- coding: utf-8 -*-

{
    'name': 'Hospital Management',
    'version': '1.0.0',
    'category': 'Hospital',
    'summary': 'hospital management system',
    'description': """hospital management system""",
    'depends': ['base', 'mail', 'product', 'sale', 'report_xlsx'],  # install these modules automatic when install my module
    'excludes': [''],                                         # to prevent install module => excludes: ['module_name', ..]
    'data': [
        "security/ir.model.access.csv",
        "data/patient_tag_data.xml",
        "data/hospital.patient.tag.csv",
        "data/sequence_data.xml",
        "data/sequence_appointment.xml",
        "data/hospital.country.csv",
        "data/hospital.city3.csv",
        "data/mail_template_data.xml",
        "wizard/cancel_appointment_view_2.xml",
        "wizard/sale_order_duration_view.xml",
        "wizard/create_appointment.xml",
        "views/menu.xml",
        "views/patient_view.xml",
        "views/female_patient_view.xml",
        "views/appointment_view.xml",
        "views/doctors.xml",
        "views/tags.xml",
        'views/sale_order_view.xml',
        'views/odoo_playground_view.xml',
        'views/res_config_settings_views.xml',
        'views/countreis_view.xml',
        'views/city_view.xml',
        'views/operation.xml',
        'views/account_move.xml',
        'views/res_partner_category.xml',
        'report/patients_report.xml',
        'report/patients_report_template.xml',
        'report/orders_report_template.xml',
        'report/appointment_report.xml',
    ],
    'demo': [],
    'auto_install': False,
    'license': 'LGPL-3',
    'application': True,
    'sequence': 1,
    'author': 'Odoo Mate'
}

