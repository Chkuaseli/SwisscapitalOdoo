from odoo import http
from odoo.http import request


class Company(http.Controller):

    @http.route('/employee/', type='http', auth="none", website=True)
    def company_employee(self, **kw):
        employee = request.env['company.employee'].search([])
        emp=[]
        for empl in employee:
            print('employee: ',employee)
            emp.append(empl)
            return emp[0].first_name
        return "hello controler you have a same exception"