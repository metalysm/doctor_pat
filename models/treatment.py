from odoo import api, fields, models


class Treatment(models.Model):
    _name = "hospital.treatment"
    _description = "Treatment"

    name = fields.Char(string='Name')
    is_done = fields.Boolean(string='Is Done')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
