from odoo import fields,models,api
from odoo.exceptions import ValidationError
from datetime import date,datetime,timedelta
from odoo.http import request
from odoo import tools

class Employeecard(models.Model):
    _name = "company.employee.employeecard"
    _auto = False
    first_name = fields.Char(string="Name")
    last_name = fields.Char(string="Last Name")
    age = fields.Integer(string="age")
    cit = fields.Char(string="Cit")
    gender =  fields.Char(string="Gender")
    personal_no =  fields.Char(string="Personal NO")
    birth_of_date = fields.Date(string="Birth Date")
    date_of_expiry = fields.Date(string="Date Expiry")
    card_no = fields.Char(string="Card No")
    signature = fields.Binary(string="Signature Image",help = "Signature")
    place_of_birth = fields.Char(string="Place of birth")
    date_of_issue = fields.Date(string="Date of Issue")
    issuing_autority = fields.Char(string="Issuing Autority")
    profile=fields.Binary(string="Profile Image" )
    date_crated = fields.Date(string="Birth Created")
    department_name = fields.Char(string="Department Name")
    human_feature = fields.Char(string="Feature")
    contract = fields.Char(string="Contract code")


    def init(self):
            tools.drop_view_if_exists(self.env.cr, 'company_employee_employeelist')
            self.env.cr.execute("""
                CREATE OR REPLACE VIEW company_employee_employeelist AS (
                    SELECT
                        row_number() OVER () AS id,
                        ce.first_name as first_name,
                        ce.last_name as last_name,
                        ce.gender as gender,    
                        ce.personal_no As personal_no, 
                        cd.name as department_name,
                        cc.code as code
                        from company_employee ce 
                        left join company_department cd on ce.department_id = cd.id 
                        left join company_contract cc on cc.employee_id = ce.id
                        left join employee_fetaure_rel efr on efr.employee_id = ce.id
                        left join company_feature cf on efr.feture_id = efr.employee_id
                    )""")

