from odoo import models, fields, api


class Invoice(models.Model):
    _name = 'account.move'
    _inherit = 'account.move'

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')  # one2many another
    appointment_ids = fields.One2many('hospital.appointment', 'account_move_id')  # ayarla. 2 field olacak her birinde.
    appointment_count = fields.Integer(string='Appointment', compute='_compute_appointment_count')
    invoice_count = fields.Integer(string='Invoice', compute='_compute_invoice_count')

    # invoice_ids = fields.One2many('account.move', 'appointment_id', string='Invoices', store=True)

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
        print('create method ')  # deniyoruz bişiler
        print('valssssss')
        print(vals)
        rec = super(Invoice, self).create(vals)
        return rec
