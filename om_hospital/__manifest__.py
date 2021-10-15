{
    'name': 'Hospital Management',
    'version': '1.0',
    'category': 'Productivity',
    'summary':'Hospital Management Software',
    'sequence': -100,
    'description': 'Hospital Management Software',
    'depends': ['sale',
                'mail',
                ],
    'license':'LGPL-3',
    'website':'https://HuynhCuongEm.vn',
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/patient_view.xml',
        'views/sale.xml',
        'views/appointments_view.xml',
        'views/doctors_view.xml',
        'views/kids_view.xml',
        'views/patient_gender_view.xml',
        'wizard/create_appointment.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False
}