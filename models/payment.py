from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Payment(models.Model):
    _name = "hospital.payment"
    _description = "Hospital Payment"
    #_rec_name = "full_name"

    total_amount = fields.Char(string=' Total Amount', store=True, compute='_compute_total_amount')
    # pending_amount = fields.Char(string=' Pending Amount', store=True, compute='_compute_pending_amount')
    sale_order_line_ids = fields.One2many('sale.order.line', 'order_id', string="Sale Order Lines")
    # sale_order_count = fields.Integer(string="Sale Orders", compute="_compute_sale_order_count")
    # invoice_count = fields.Integer(string="Invoices", compute="_compute_invoice_count")
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
