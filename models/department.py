from odoo import api, fields, models
from odoo import exceptions


class Department(models.Model):
    _name = "hospital.department"
    _description = "Department"
    _rec_name = "name"

    name = fields.Char(string='Department Name', index=True)
    code = fields.Char(string='Code', index=True, readonly=1)
    doctor_id = fields.One2many('hospital.doctor', 'department_id', string="Doctors")

    _sql_constraints = [
        ('unique_code', 'unique(code)', 'Code must be unique.'),
    ]

    @api.model
    def create(self, vals):
        print("Department create vals ", vals)
        vals['code'] = self.env['ir.sequence'].next_by_code("hospital.department")
        return super(Department, self).create(vals)
