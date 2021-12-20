{
    'name': 'Staff Management',
    'version': '1.0',
    'category': 'Productivity',
    'summary':'Staff Management Software',
    'sequence': -100,
    'description': 'Staff Management Software',
    'depends': [
        'mail',
        'hr'
    ],
    'license':'LGPL-3',
    'website':'https://HuynhCuongEm.vn',
    'data': [
        'views/employess_view.xml',
        'views/department_view.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False
}