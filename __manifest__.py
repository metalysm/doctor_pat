# -*- coding: utf-8 -*-

{
    'name': 'DoktorHasta',
    'version': '1.0.0',
    'category': 'DokiDoki',
    'author': 'burak',
    'sequence': -100,
    'summary': 'summer i',
    'description': """asdas""",
    'depends': ['base', 'mail', 'sale', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/patient_view.xml',
        'views/doctor_view.xml',
        'views/appointment_view.xml',
        'views/department_view.xml',
        'views/treatment_view.xml',
        'views/invoice_view.xml',
        # 'views/payment_view.xml',
        'views/sale_order_view.xml',
        'views/menu.xml',
        'wizard/create_appointment_view.xml',
        'wizard/search_appointment_view.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}