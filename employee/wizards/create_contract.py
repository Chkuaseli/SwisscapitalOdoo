from odoo import fields,models,api
from odoo.exceptions import ValidationError
from datetime import date

class Contract(models.TransientModel):
    _name = "create.contract"
    # get default value
    @api.model
    def default_get(self,fields):
        res = super(Contract, self).default_get(fields)
        if self._context.get('active_id'):
            res['employee_id'] = self._context.get('active_id')
        print("ressssss",res)
        return res

    employee_id = fields.Many2one("company.employee", string="Employee")
    code = fields.Char(string="Contract code: ",required=True)
    start_date = fields.Date(string="Start date: ",required=True , default = fields.Date.today())
    end_date = fields.Date(string="End date: ",required=True)

    def create_contract(self):
        print("button clicked")
        vals = {
            'employee_id' : self.employee_id.id,
            'code' : self.code,
            'start_date' : self.start_date,
            'end_date' : self.end_date
        }
        self.env['company.contract'].create(vals)
        print("valsss",vals)
             
    

