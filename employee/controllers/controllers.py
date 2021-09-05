from odoo import http
from odoo.http import requests

class Company(http.Controller):

    @http.route('/employee/', type='http', auth="user", website=True)
    def company_employee(self, **kw):
        print("can loadinggggggggggggggggggggggg")
        employee = {
            "name":"tariel","last_name":"chkuaseli"
            }
        if employee:
            return employee
        return "hello word"