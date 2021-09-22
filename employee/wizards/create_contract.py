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
   
    # create contarct
    def create_contract(self):
        print("button clicked create contract")
        vals = {
            'employee_id' : self.employee_id,
            'code' : self.code,
            'start_date' : self.start_date,
            'end_date' : self.end_date
        }
        self.env['company.contract'].create(vals)

    @api.constrains('start_date')
    def validate_start_date(self):
        today = date.today()
        for record in self:
            if record.start_date != today:
                raise ValidationError("Contract must be start from %s!" % today)
            if record.start_date > self.end_date:
                raise ValidationError("Contract start date must be greather then contract end date! ")
    
    @api.constrains('end_date')
    def validate_end_date(self):
        today = date.today()
        for record in self:
            if record.end_date <= today:
                raise ValidationError("Not valid date end date must be greather %s! " %today)
            if record.end_date <= self.start_date:
                raise ValidationError("Not valid contact end date check %s!" %record.end_date)

    
    
    # update contract
    def update_contract(self):
        print("button clicked Update contract")
        # res = super(Contract, self).default_get(fields)
        # if self._context.get('active_id'):
        #     res['employee_id'] = self._context.get('active_id')
        vals = {
            'employee_id' : self.employee_id,
            'code' : self.code,
            'start_date' : self.start_date,
            'end_date' : self.end_date
        }
        # self.code = self.env['company.contract'].search(['id','=',self._context.get("active_id")]).code

        self.env["company.contract"].search([("employee_id","=",self._context.get("active_id"))]).create(vals)
   
    # delete contract 
    def delete_contract(self):
        print("stars deleting")
        print("delete contract id is:",self.env["company.contract"].search([("employee_id","=",self._context.get("active_id"))]))
        self.env["company.contract"].search([("employee_id","=",self._context.get("active_id"))]).unlink()
      
        print("deleted successfully")
            


