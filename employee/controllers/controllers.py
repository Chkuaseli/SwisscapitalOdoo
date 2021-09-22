from odoo import http
from odoo.http import request


class Company(http.Controller):

    @http.route('/employee/', type='http', auth='public', website=True)
    def company_employee(self, **kw):
        datas = request.env["company.employee"].sudo().search([])
        return request.render("employee.employee_page",{
            'datas':datas
            }
        )