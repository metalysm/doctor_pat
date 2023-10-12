from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    appointment_count = fields.Integer(string='Appointment', compute='_compute_appointment_count', store=True)
    invoice_count = fields.Integer(string='Invoice', compute='_compute_invoice_count')
    invoice_ids = fields.One2many('account.move', 'appointment_id', string='Invoice')

    @api.depends('appointment_id')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_id) if rec.appointment_id else 0


    # def action_view_appointment(self):
    #     self.ensure_one()
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Appointment',
    #         'view_mode': 'form',
    #         'res_model': 'hospital.appointment',
    #         'res_id': self.appointment_id.id,
    #         'context': {'create': True, 'edit': False},
    #         'target': 'current',
    #     }

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for appointment in self:
            appointment.invoice_count = len(appointment.invoice_ids)

    def action_open_appointments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment',
            'view_mode': 'form',
            'res_model': 'hospital.appointment',
            'res_id': self.appointment_id.id,
            'context': {'create': True, 'edit': False},
            'target': 'current',
        }

    # def action_open_invoice(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Appointments',
    #         'res_model': 'account.move',
    #         'domain': [('patient_id', '=', self.id)],
    #         'context': {'default_patient_id': self.id},
    #         'view_mode': 'tree,form',
    #         'target': 'current',
    #     }

    # def action_view_sale_appointment(self):
    #     self.ensure_one()
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Appointment',
    #         'view_mode': 'form',
    #         'res_model': 'hospital.appointment',
    #         'res_id': self.appointment_id.id,
    #         'context': {'create': False, 'edit': False},
    #         'target': 'current',
    #     }

    def action_view_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('appointment_id', '=', self.id)],
            'context': {'default_appointment_id': self.id},
            # 'target': 'current',
        }
