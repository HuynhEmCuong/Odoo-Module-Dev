{
    'name': 'Asset Management',
    'version': '1.0',
    'category': 'Productivity',
    'summary':'Asset Management Software',
    'sequence': -100,
    'description': 'Asset Management Software',
    'depends': [
        'product',
        'mail',
        'stock',

    ],
    'license':'LGPL-3',
    'website':'https://HuynhCuongEm.vn',
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/asset_view_menu.xml',
        'views/wearhouse_view.xml',
        'views/wearhouse_in_view.xml',
        'views/wearhouse_view_overview.xml',
        'views/block_view.xml',
        'views/dept_view.xml',
        'views/room_view.xml',
        'views/product_move_room_view.xml',
        'views/product_category_view.xml',
        'report/report_wearhouse.xml',
        'report/report_wearhouse_template.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False
}