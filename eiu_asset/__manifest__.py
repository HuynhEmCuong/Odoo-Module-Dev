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
        'account',
        'hr'

    ],
    'license':'LGPL-3',
    'website':'https://HuynhCuongEm.vn',
    'data': [
        'security/security.xml',
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
        'views/qr_code_invoice.xml',

        'views/account_move_view.xml',
        'views/asset_style.xml',
        'views/stock_move.xml',


        'report/report_wearhouse.xml',
        'report/report_wearhouse_template.xml',

        'wizard/create_qrcode.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False
}