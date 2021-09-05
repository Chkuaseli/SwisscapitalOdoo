from odoo import fields,models,api
from odoo.exceptions import ValidationError
from datetime import date,datetime,timedelta

class Employee(models.Model):
    _name = "company.employee"
    _description ="Company Employee"

    first_name = fields.Char(string="Name",required=True)
    last_name = fields.Char(string="Last Name",required=True)
    cit = fields.Char(string="Cit",required=True)
    gender = fields.Selection([("M","Male"),("F","Female")],help="Gender",required=True)
    personal_no = fields.Char(string="Personal No",required=True) # აქ integer არ გამოვიყენე რადგან მის რეინჯში არ ეტეოდა და bigint უნდა გამომეყენებინა რომლისთვისაც ახალი პაკეტი უნდა ჩამომეწერა ამიტომ თავი შევიკავე და ვალიდაციებში გამოვიყვან
    birth_of_date = fields.Date(string="Birth Date",required=True)
    date_of_expiry = fields.Date(string="Date Expiry",required=True)
    card_no = fields.Char(string="Card No",required=True)
    signature = fields.Binary(string="Signature Image",max_width = 100,max_height = 100,help = "Signature",required=True)
    place_of_birth = fields.Char(string="Place of birth",required=True)
    date_of_issue = fields.Date(string="Date of Issue",required=True)
    issuing_autority = fields.Char(string="Issuing Autority",required=True)
    profile=fields.Binary(string="Profile Image" ,max_width = 100,max_height = 100,help = "Profile image",required=True)
    date_crated = fields.Date(string="Birth Created",required=True)
    department_id = fields.Many2one('company.department', string="Department", required=True)
    feature_list = fields.Many2many("company.feature", 'employee_fetaure_rel', 'employee_id', 'feture_id', string = "Human Features",required=True)

    # unique data "personal_no","card_no"
    _sql_constraints = [
        ('personal_no_unique', 'unique(personal_no)', 'Can not be duplicate value for Personal Card No!'),
        ('card_no_unique', 'unique(card_no)', 'Can not be duplicate value for Personal Card Code!')
        ]

    # validate personal no
    @api.onchange('personal_no')
    def validate_personal_no(self):
        for record in self:
            if record.personal_no != False:
                print("Personal number validation data is: ",record.personal_no)
                if record.personal_no.isdigit() == False:
                    raise ValidationError('Personal No must be number! ')
                if len(record.personal_no) != 11:
                    raise ValidationError('Personal number must be 11 digit! ')

     # validate birth of date
    @api.onchange('birth_of_date')
    def validate_birth_of_date(self):
        today = date.today()
        for record in self:
            if record.birth_of_date != False:
                if record.birth_of_date > today:
                    raise ValidationError("Imposible value for birt of date!")
                if record.birth_of_date < date(1900, 1, 1):
                    raise ValidationError("Imposible value !!! You are always alive ?")
    
    # validate exspiry date 
    @api.onchange('date_of_expiry','birth_of_date','date_of_issue')
    def validate_date_of_expiry(self):
        today = date.today()
        for record in self:
            if record.birth_of_date != False and record.date_of_expiry != False and record.date_of_issue != False:
                age = today.year - record.birth_of_date.year - ((today.month, today.day) <(record.birth_of_date.month, record.birth_of_date.day))
                range_of_ex = record.date_of_expiry  - record.date_of_issue
                max = date.today() + timedelta(10*365+2)
                print("es aris vadaaa piradobis: ",range_of_ex)
                #data must be range "curent data" and "curent data + 10 year"
                if record.date_of_expiry < today or record.date_of_expiry > max:
                    raise ValidationError("This Expity date is up to data")
                if age < 18 and range_of_ex != timedelta((4*365)+1):
                    raise ValidationError('This Card ID is expired your or entered data is incorrectly ')
                if range_of_ex % timedelta(2) == timedelta(0):
                    if age >= 18 and range_of_ex != timedelta(((10 * 365)+2)):
                        print("one err: ",range_of_ex,type(range_of_ex))
                        raise ValidationError('This Card ID is expired your or entered data is incorrectly ')
                if range_of_ex % timedelta(2) != timedelta(0):
                    if age >= 18 and range_of_ex != timedelta(((10 * 365)+3)):
                        print('two err :',range_of_ex % timedelta(2) )
                        raise ValidationError('This Card ID is expired your or entered data is incorrectly ')
   
    # validate card code
    @api.onchange('card_no')
    def validate_card_no(self):
        for record in self:
            if record.card_no != False:
                print(record.card_no)
                if record.card_no[2:3].isdigit()== True or record.card_no[3:4].isdigit() == True or (record.card_no[:2] + record.card_no[4:]).isdigit() == False:
                    raise ValidationError('This ID Card code format not exist! Correct Format: 12IB11111 ')
                if len(record.card_no) != 9:
                    raise ValidationError('Personal Card No must be 9 characters! ')
            return None

    @api.onchange('date_of_issue','birth_of_date')
    def validate_date_of_issue(self):
        today = date.today()
        for record in self:
            max = date.today() - timedelta(10*365+2)
            if record.date_of_issue != False and record.birth_of_date != False:
                age = today.year - record.birth_of_date.year - ((today.month, today.day) <(record.birth_of_date.month, record.birth_of_date.day))
                issue = today - record.date_of_issue
                if record.date_of_issue > today or record.date_of_issue < max:
                    raise ValidationError('This ID Card is expired your card DATE OF DATE must be less then today')
                if age < 18 and issue >= timedelta((4*365)+1):
                    print("first record: ",record.date_of_issue)
                    raise ValidationError('This ID Card is expired or your entered data is incorrectly ')
                if age >= 18 and issue > timedelta(((10 * 365)+2)):
                    print("second record",record.date_of_issue)
                    raise ValidationError('This ID Card is expired or your entered data is incorrectly ')


class Department(models.Model):
    _name = "company.department"
    _description ="Company departments"
    
    name = fields.Char(string="Department name",required=True)
    description = fields.Text(string="Description",required=True)
    employee_id = fields.One2many('company.employee', 'department_id', string='Employee')

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Can not be duplicate value for Department name!')]

class Feature(models.Model):
    _name = "company.feature"
    _description ="Company Employee's Feature"

    name = fields.Char(string="Human Feature",required=True)
    description = fields.Text(string="Description",required=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Can not be duplicate value for Feature name!')]
