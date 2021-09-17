from odoo import models, fields, api
from odoo import tools


class Employeeanalysis(models.Model):
    _name = 'company.employee.employeeanalysis'
    _auto = False
    _description = 'Employee Sale Analysis'
    emp_feature = fields.Char(string="human feature")
    total_feature = fields.Integer(string="total_feature")
    total_gender = fields.Integer(string="total_gender")
    gender = fields.Selection([("M","Male"),("F","Female")],help="Gender")
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