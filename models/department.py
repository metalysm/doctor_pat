from odoo import api, fields, models
from odoo import exceptions


class Department(models.Model):
    _name = "hospital.department"
    _description = "Department"
    _rec_name = "name"

    name = fields.Char(string='Department Name', index=True)
    code = fields.Char(string='Code', index=True)
    doctor_id = fields.One2many('hospital.doctor', 'department_id', string="Doctors")

    _sql_constraints = [
        ('unique_code', 'unique(code)', 'Code must be unique.'),
    ]

    # @api.constrains('code')
    # def _check_unique_code(self):
    #     for rec in self:
    #         if self.search_count([('code', '=', rec.code)]) > 1:
    #             raise exceptions.ValidationError("Code must be unique.")

    # @api.model
    # def create(self, vals):
    #     if 'code' in vals and not vals.get('name'):
    #         vals['name'] = vals['code']
    #     return super(Department, self).create(vals)