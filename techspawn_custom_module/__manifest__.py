# -*- coding: utf-8 -*-
{
    'name': "TechSpawn Task",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Paidy Kumar",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'sale_management', 'report_xlsx'],

    # always loaded
    'data': [
        'views/sale_order.xml',
        'views/report_custom_sale_order.xml',
        'views/res_config_settings.xml',
        'views/sale_order_line.xml',
    ],

}
