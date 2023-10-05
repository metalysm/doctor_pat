from odoo import api, fields, models
from odoo import exceptions


class Doctor(models.Model):
    _name = "hospital.doctor"
    _description = "Hospital Doctor"
    _rec_name = "full_name"

    first_name = fields.Char(string=' First Name')
    last_name = fields.Char(string=' Last Name')
    full_name = fields.Char(string=' Full Name', store=True, compute='_compute_full_name')
    date_of_birth = fields.Date(string="Date of Birth", store=True)
    age = fields.Integer(string='Age', required=True, readonly=True, compute='_compute_age')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    department_id = fields.Many2one(comodel_name='hospital.department', string='Department')
    start_time = fields.Float(string='Start Time', widget="float_time")
    end_time = fields.Float(string='End Time', widget="float_time")
    image = fields.Binary(string="Patient Image")
    active = fields.Boolean(string="Active", default=True)

    # @api.onchange('department_id')
    # def _onchange_department(self):
    #     self.write({
    #         'name': self.department_id.name,
    #         'code': self.department_id.code
    #     })

    @api.constrains('email')
    def _check_unique_email(self):
        for rec in self:
            if self.search_count([('email', '=', rec.email)]) > 1:
                raise exceptions.ValidationError("Email address must be unique.")

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for rec in self:
            rec.full_name = rec.first_name + ' ' + rec.last_name

    @api.onchange('date_of_birth')
    def _compute_age(self):
        for rec in self:
            if rec.date_of_birth:
                rec.age = fields.Date.today().year - rec.date_of_birth.year

    # def _compute_appointment_count(self):
    #     for rec in self:
    #         appointment_count = self.env['hospital.appointment'].search_count([('doctor_id', '=', rec.id)])
    #         rec.appointment_count = appointment_count
