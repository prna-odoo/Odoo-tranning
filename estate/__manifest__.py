{
    'name': "Real Estate",
    'version': '15.0.1.0.0',
    'category': 'Category',
    'depends': ['website'],
    'author': "Pravin Nayee",
    'license': 'LGPL-3',
    'summary': 'Real estate module',
    'description': """ Module for sale of real estate proper
    """,
    'website': 'https://WWW.odoo.com',
    # data files always loaded at installation
    'data': [
        "security/ir.model.access.csv",
        "security/security.xml",
        "views/estate_menus.xml",
        "views/estate_property_views.xml",
        "wizard/property_wizard_view.xml",
        "data/estate_property_data.xml",
        "views/estate_templates.xml",

    ],

    'installable': True,
    'auto_install': False,
    'application': True,

}
