from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment') #one2many  smart button'da hep bu.
    # 2.kural ilkte hep tree view açılır sonra form view açılır.
    appointment_count = fields.Integer(string='Appointment', compute='_compute_appointment_count', store=True)
    invoice_count = fields.Integer(string='Invoice', compute='_compute_invoice_count')
    invoice_ids = fields.One2many('account.move', 'appointment_id', string='Invoice', compute="_compute_invoice_ids",
                                  store="True")


    @api.depends('appointment_id')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_id) if rec.appointment_id else 0

    @api.depends('appointment_id')
    def _compute_invoice_ids(self):
        for rec in self:
            rec.invoice_ids = self.env['account.move'].search([('appointment_id', '=', rec.id)])

    @api.depends('invoice_ids', 'appointment_id')
    def _compute_invoice_count(self):
        for rec in self:
            rec.invoice_count = len(rec.invoice_ids)

    def action_open_appointments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment',
            'view_mode': 'tree,form',
            'res_model': 'hospital.appointment',
            'res_id': self.appointment_id.id,
            'context': {'create': True, 'edit': False},
            'target': 'current',
        }

    def action_open_invoice(self):
        self.ensure_one()

        # Create a new invoice
        invoice_id = self.env['account.move'].create({
            'appointment_id': self.appointment_id.id,  # Set the appointment on the invoice
            # Other fields for the invoice, such as partner_id, product lines, etc.
        })

        # Open the created invoice in form view
        print(invoice_id)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'res_id': invoice_id.id,
            'context': {'create': False, 'edit': False},
            'view_mode': 'tree,form',
            'target': 'current',
        }

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
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_move_form').id,
            'res_model': 'account.move',
            'domain': [('appointment_id', '=', self.id)],
            'context': {'default_appointment_id': self.id},
            'target': 'current',
        }


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
