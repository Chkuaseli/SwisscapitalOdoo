{
    "name":"Company",
    'description':'company information',
    'version' : '1.0',
    'category': 'administration',
    'secuence': - 100,
    'depends' : [],
    'data': [
        'security/ir.model.access.csv',
        'views/view.xml',
        'views/template.xml',
        'views/company_employee_analyse.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}