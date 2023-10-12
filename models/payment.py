from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Payment(models.Model):
    _inherit = "account.payment"

    total_amount = fields.Char(string=' Total Amount', store=True, compute='_compute_total_amount')
    payment_count = fields.Integer(string="Payments", compute="_compute_payment_count")

    @api.depends('sale_order_line_ids.payment_ids')
    def _compute_payment_count(self):
        for rec in self:
            rec.payment_count = len(rec.sale_order_line_ids.mapped('payment_ids'))

    @api.depends('sale_order_line_ids')
    def _compute_total_amount(self):
        for rec in self:
            total_amount = sum(rec.sale_order_line_ids.mapped('price_total'))
            rec.total_amount = total_amount

    def button_open_journal_entry(self):
        ''' Redirect the user to this payment journal.
        :return:    An action on account.move.
        '''
        self.ensure_one()
        return {
            'name': _("Journal Entry"),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'context': {'create': False},
            'view_mode': 'form',
            'res_id': self.move_id.id,
        }

    def action_open_destination_journal(self):
        ''' Redirect the user to this destination journal.
        :return:    An action on account.move.
        '''
        self.ensure_one()

        action = {
            'name': _("Destination journal"),
            'type': 'ir.actions.act_window',
            'res_model': 'account.journal',
            'context': {'create': False},
            'view_mode': 'form',
            'target': 'new',
            'res_id': self.destination_journal_id.id,
        }
        return action




    # def action_sale_order(self):
    #     for appointment in self:
    #         sale_order_values = {
    #             'partner_id': appointment.patient_id.id,
    #             'date_order': appointment.appointment_date_time,
    #             # Diğer gerekli bilgileri burada ekleyin
    #         }
    #         print("Sale Order Oluşturuldu")
    #
    #         sale_order = self.env['sale.order'].create(sale_order_values)
    #
    #         # Satış siparişini düzenleme
    #         self.env.context = dict(self.env.context, default_sale_order_id=sale_order.id)
    #         return {
    #             'name': 'Sale Order',
    #             'type': 'ir.actions.act_window',
    #             'res_model': 'sale.order',
    #             'res_id': sale_order.id,
    #             'view_mode': 'form',
    #             'target': 'current',
    #         }
