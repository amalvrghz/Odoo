{
    'name': "SO Approval",
    'depends': ['base', 'sale_management'],
    'application': True,
    'version': '15.0.1.0.0',
    'sequence': 3,
    'summary': 'Sale Order Approval',
    'description': "",
    'license': '',
    'website': '',
    'data': [
        'security/ir.model.access.csv',
        'security/user_groups.xml',
        'views/so_approval.xml'

    ]
}