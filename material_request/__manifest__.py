{
    'name': "Material Request",
    'depends': ['base', 'stock'],
    'application': True,
    'version': '15.0.1.0.0',
    'sequence': 2,
    'summary': 'Request for Materials',
    'description': "Material Request",
    'license': '',
    'website': '',
    'data': [
        'security/ir.model.access.csv',
        'security/user_groups.xml',
        'views/material_request.xml',
        'data/sequence.xml',

    ]
}