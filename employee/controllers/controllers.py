from odoo import http
from odoo.http import request,Response
import json
from json import JSONEncoder
import datetime

def myconverter(o):
    if isinstance(o, datetime.date):
        return o.__str__()

class EmployeeEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return o.__str__()
        return o.__dict__

class Company(http.Controller):

    @http.route('/', type='http', auth='public', website=True,method='GET')
    def company_employee(self, **kw):
        datas = request.env["company.employee"].sudo().search([])
        return request.render("employee.employees",{
            'datas':datas
            }
        )

class Employee(http.Controller):
    @http.route("/employee_json/", auth='public', type='http',method=['GET'],website=True)
    def employee_json(self,**values):
        datas = request.env["company.employee"].search([])
        all_data=[]
        for emp in datas:
            output = {
                'name':emp.first_name,
                'Last Name':emp.last_name,
                'age':emp.age,
                'cit':emp.cit,
                'gender':emp.gender,
                'personal number':emp.personal_no,
                'birthdate':emp.birth_of_date,
                'card number':emp.card_no,
                'place of birth':emp.place_of_birth,
                'date of issue':emp.date_of_issue,
                'issuing autority':emp.issuing_autority,
                'department':emp.department_id.name,
                'human feature':[em.name for em in emp.feature_list],
                'contracts':[[e.name for e in em.contracts_list] for em in emp.contract_id] 
                }
            all_data.append(output)
            print("alldata",all_data)
        return Response(json.dumps(all_data,indent=4, cls=EmployeeEncoder,default=myconverter),
        content_type='application/json;charset=utf-8',status=200
        
        )
