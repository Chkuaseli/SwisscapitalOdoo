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
    contracts_list = fields.Many2many("company.companycontracts", 'contractwizard_companycontracts_rel', 'contractwizard_id', 'companycontracts_id', string = "Company Contract")
    start_date = fields.Date(string="Start date: ",required=True , default = fields.Date.today())
    end_date = fields.Date(string="End date: ",required=True)
   
    # create contarct
    def create_contract(self):
        print("button clicked create contract")
        cont = [i.id for i in self.contracts_list]
        print("contttttttttttt",cont)
        vals = {
            'employee_id' : self.employee_id,
            'contracts_list' : [[6, 0, [i.id for i in self.contracts_list]]], 
            'start_date' : self.start_date,
            'end_date' : self.end_date
        }
        m = self.env['company.contract']
        m.sudo().create(vals)
        # for rec in self.contracts_list:
        #     m.create({'contracts_list' :str( rec.id)})

    @api.constrains('start_date','end_date')
    def validate_start_date(self):
        today = date.today()
        for record in self:
            if record.start_date != today:
                raise ValidationError("Contract must be start from %s!" % today)
            if record.end_date != False:
                if record.start_date > record.end_date:
                    raise ValidationError("Contract start date must be greather then contract end date! ")
    
    @api.constrains('end_date')
    def validate_end_date(self):
        today = date.today()
        for record in self:
            if record.end_date != False:
                if record.end_date <= today:
                    raise ValidationError("Not valid date end date must be greather %s! " %today)
                if record.end_date <= self.start_date:
                    raise ValidationError("Not valid contact end date check %s!" %record.end_date)

    
    
    # update contract
    def update_contract(self):
        print("button clicked Update contract")
        vals = {
            'employee_id' : self.employee_id,
            'contracts_list' : [[6, 0, [i.id for i in self.contracts_list]]],
            'start_date' : self.start_date,
            'end_date' : self.end_date
        }
        try:
            self.env["company.contract"].search([("employee_id","=",self._context.get("active_id"))]).write(vals)
        except Exception as e:
            print("try cach exception: ",e)
    
    # delete contract 
    def delete_contract(self):
        print("stars deleting")
        print("delete contract id is:",self.env["company.contract"].search([("id","=",self._context.get("active_id"))]))
        self.env["company.contract"].search([("id","=",self._context.get("active_id"))]).unlink()
      
        print("deleted successfully")
            


