from odoo import api, fields, models


class Treatment(models.Model):
    _name = "hospital.treatment"
    _description = "Treatment"
    _rec_name = "name"

    name = fields.Char(string='Name', index=True)
    is_done = fields.Boolean(string='Is Done')
    appointment_id = fields.One2many('hospital.appointment', 'treatment_id', string='Appointment')
