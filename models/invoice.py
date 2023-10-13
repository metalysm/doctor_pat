from odoo import models, fields, api


class Invoice(models.Model):
    _name = 'account.move'
    _inherit = 'account.move'

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    appointment_count = fields.Integer(string='Appointment', compute='_compute_appointment_count')
    invoice_count = fields.Integer(string='Invoice', compute='_compute_invoice_count')
    invoice_ids = fields.One2many('account.move', 'appointment_id', string='Invoices', store=True)

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

    # def action_view_payments(self):
    #     self.ensure_one()
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Invoices',
    #         'view_mode': 'tree,form',
    #         'res_model': 'account.payment',
    #         'domain': [('id', 'in', self.invoice_ids.ids)],
    #         'context': {'create': False, 'edit': False},
    #         'target': 'current',
    #     }

    # def action_view_payment(self):
    #     self.ensure_one()
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Invoices',
    #         'view_mode': 'tree,form',
    #         'res_model': 'account.payment',
    #         'domain': [('invoice_ids', '=', self.id)],
    #         'context': {'default_invoice_ids': self.id},
    #         'target': 'current',
    #     }




##########################################################

# ESKİSİ


# from odoo import api, fields, models, _
# from odoo.exceptions import ValidationError
#
#
# class Invoice(models.Model):
#     _name = "hospital.invoice"
#     _description = "Hospital Invoice"
#     #_rec_name = "full_name"
#
#
#     # total_amount = fields.Char(string=' Total Amount', store=True, compute='_compute_total_amount')
#     pending_amount = fields.Char(string=' Pending Amount', store=True, compute='_compute_pending_amount')
#     sale_order_line_ids = fields.One2many('sale.order.line', 'order_id', string="Sale Order Lines")
#     # sale_order_count = fields.Integer(string="Sale Orders", compute="_compute_sale_order_count")
#     invoice_count = fields.Integer(string="Invoices", compute="_compute_invoice_count")
#     # payment_count = fields.Integer(string="Payments", compute="_compute_payment_count")
#
#
#
#     # @api.depends('sale_order_line_ids.order_id')
#     # def _compute_sale_order_count(self):
#     #     for rec in self:
#     #         rec.sale_order_count = len(rec.sale_order_line_ids.mapped('order_id'))
#     #
#
#
#     @api.depends('sale_order_line_ids.invoice_status')
#     def _compute_invoice_count(self):
#         for rec in self:
#             rec.invoice_count = len(
#                 rec.sale_order_line_ids.filtered(lambda line: line.invoice_status == 'invoiced'))
#
#     @api.depends('sale_order_line_ids', 'sale_order_line_ids.invoice_status')
#     def _compute_pending_amount(self):
#         for rec in self:
#             pending_amount = sum(
#                 rec.sale_order_line_ids.filtered(lambda line: line.invoice_status != 'invoiced').mapped(
#                     'price_total'))
#             rec.pending_amount = pending_amount
#
#     def action_view_invoice(self):
#         return {
#             'name': _('Invoice'),
#             'res_model': 'account.invoice.send',
#             'view_mode': 'form',
#             'context': {
#                 'default_template_id': self.env.ref(self._get_mail_template()).id,
#                 'mark_invoice_as_sent': True,
#                 'active_model': 'account.move',
#                 # Setting both active_id and active_ids is required, mimicking how direct call to
#                 # ir.actions.act_window works
#                 'active_id': self.ids[0],
#                 'active_ids': self.ids,
#                 'custom_layout': 'mail.mail_notification_paynow',
#             },
#             # 'domain': [('patient_id', '=', '')]
#             'target': 'new',
#             'type': 'ir.actions.act_window',
#         }
#
#     # def action_sale_order(self):
#     #     for appointment in self:
#     #         sale_order_values = {
#     #             'partner_id': appointment.patient_id.id,
#     #             'date_order': appointment.appointment_date_time,
#     #             # Diğer gerekli bilgileri burada ekleyin
#     #         }
#     #         print("Sale Order Oluşturuldu")
#     #
#     #         sale_order = self.env['sale.order'].create(sale_order_values)
#     #
#     #         # Satış siparişini düzenleme
#     #         self.env.context = dict(self.env.context, default_sale_order_id=sale_order.id)
#     #         return {
#     #             'name': 'Sale Order',
#     #             'type': 'ir.actions.act_window',
#     #             'res_model': 'sale.order',
#     #             'res_id': sale_order.id,
#     #             'view_mode': 'form',
#     #             'target': 'current',
#     #         }
