from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _name = "sale_order"
    _description = "Hospital Sale Order"
    # _rec_name = "full_name"

    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count')

    # def _compute_goto_appointment(self):
    #     for rec in self:
    #         goto_appointment = self.env['hospital.appointment'].search_count([('doctor_id', '=', rec.id)])
    #         rec.goto_appointment = goto_appointment
