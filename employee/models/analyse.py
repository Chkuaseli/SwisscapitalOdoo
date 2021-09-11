from odoo import models, fields, api
from odoo import tools


class Employeeanalysis(models.Model):
    _name = 'company.employee.employeeanalysis'
    _auto = False
    _description = 'Employee Sale Analysis'
    emp_feature = fields.Char(string="human feature")
    total_feature = fields.Integer(string="total_feature")
    total_gender = fields.Integer(string="total_gender")
    # cit = fields.Char(string="Cit")
    gender = fields.Selection([("M","Male"),("F","Female")],help="Gender")
    # birth_of_date = fields.Date(string="Birth Date")
    # date_of_expiry = fields.Date(string="Date Expiry")
    # place_of_birth = fields.Char(string="Place of birth")
    # date_of_issue = fields.Date(string="Date of Issue")
    # issuing_autority = fields.Char(string="Issuing Autority")
    # date_crated = fields.Date(string="Birth Created")
    # department_id = fields.Many2one('company.department', string="Department", )
    feature_list = fields.Many2many("company.feature", 'employee_fetaure_rel', 'employee_id', 'feture_id', string = "Human")

    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'company_employee_employeeanalysis')
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW company_employee_employeeanalysis AS (
                SELECT
                    row_number() OVER () AS id,
                    ce.gender as gender,
                    cf.name as emp_feature,
                    count(cf.name) as total_feature,
                    count(ce.gender) as total_gender
                    from company_employee ce 
                    left join employee_fetaure_rel efr on efr.employee_id = ce.id
                    left join company_feature cf on efr.feture_id = efr.employee_id
                    group by gender,emp_feature
                )""")