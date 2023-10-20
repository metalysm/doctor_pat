from odoo import models, fields, api


class Invoice(models.Model):
    _inherit = 'account.move'

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    appointment_ids = fields.One2many('hospital.appointment', 'account_move_id')
    appointment_count = fields.Integer(string='Appointment', compute='_compute_appointment_count')
    # payment_count = fields.Integer(string='Payment Count', compute='_compute_payment_count')
    # payment_ids = fields.One2many('account.payment', 'appointment_id', compute='_compute_payment_ids', store=True)

    @api.depends('appointment_id')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_id) if rec.appointment_id else 0

    def action_view_appointment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment',
            'view_mode': 'form',
            'res_model': 'hospital.appointment',
            'res_id': self.appointment_id.id,
            'context': {'create': False, 'edit': False},
            'target': 'current',
        }

    @api.model
    def create(self, vals):
        print('<<<<<<<create method account.move >>>>>>>')  # deniyoruz bişiler
        print("<<<<<<<<<<<<<<<<<<<vals>>>>>>>>>>>>>>>>>>>")
        print(vals)
        print(self.id)
        if 'invoice_origin' in vals and vals['invoice_origin']:
            sale_order = self.env['sale.order'].search([('name', '=', vals['invoice_origin'])])
            vals['appointment_id'] = sale_order.appointment_id.id
        rec = super(Invoice, self).create(vals)
        return rec

