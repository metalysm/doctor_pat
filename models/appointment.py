# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"

    appointment_date_time = fields.Datetime(string="Appointment Date & Time")
    code = fields.Char(string="Code", required=True, index=True, readonly=1)
    doctor_id = fields.Many2many(comodel_name='hospital.doctor', string="Doctor", required=True)
    patient_id = fields.Many2one(comodel_name='hospital.patient', string="Patient", required=True)
    stage = fields.Selection([('draft', 'Draft'), ('in-progress', 'In Progress'), ('done', 'Done'),
                              ('cancel', 'Cancel')], default='draft', string="Stage")
    treatment_id = fields.One2many('hospital.treatment', 'appointment_id', string='Treatments')
    prescription = fields.Text(string="Prescription")
    prescription_line_ids = fields.One2many('appointment.prescription.lines', 'appointment_id',
                                            string="Prescription Lines")

    appointment_id = fields.Many2one(comodel_name="sale.order", string="Sale Order")
    #
    total_amount = fields.Char(string=' Total Amount', store=True, compute='_compute_total_amount')
    pending_amount = fields.Char(string=' Pending Amount', store=True, compute='_compute_pending_amount')
    sale_order_line_ids = fields.One2many('sale.order.line', 'order_id', string="Sale Order Lines")
    sale_order_count = fields.Integer(string="Sale Orders", compute="_compute_sale_order_count")
    invoice_count = fields.Integer(string="Invoices", compute="_compute_invoice_count")
    payment_count = fields.Integer(string="Payments", compute="_compute_payment_count")
    invoice_ids = fields.One2many('account.move', 'appointment_id', string="Invoices")

    _sql_constraints = [
        ('unique_code', 'unique(code)', 'Code must be unique.'),
    ]

    #
    # PHASE 1 METHODS
    #

    def action_confirm(self):
        print("BUTTON PROGRESS")
        self.stage = 'in-progress'

    def action_done(self):
        print("BUTTON DONE")
        self.stage = 'done'

    def action_draft(self):
        print("BUTTON DRAFT")
        self.stage = 'draft'

    def action_cancel(self):
        print("BUTTON CANCEL")
        self.stage = 'cancel'

    @api.model    # generate unique codes
    def create(self, vals):
        print("Appointment create vals ", vals)
        vals['code'] = self.env['ir.sequence'].next_by_code("hospital.appointment")
        return super(HospitalAppointment, self).create(vals)

    def unlink(self):   # for undeletable done states
        if self.stage == 'done':
            raise ValidationError(_("You Cannot Delete %s as it is in Done State" % self.code))
        return super(HospitalAppointment, self).unlink()

    def action_url(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'https://apps.odoo.com/apps/modules/15.0/%s/' % self.prescription,
        }

    #
    # PHASE 2 METHODS
    #

    @api.depends('sale_order_line_ids')
    def _compute_total_amount(self):
        for rec in self:
            total_amount = sum(rec.sale_order_line_ids.mapped('price_total'))
            rec.total_amount = total_amount

    @api.depends('sale_order_line_ids', 'sale_order_line_ids.invoice_status')
    def _compute_pending_amount(self):
        for rec in self:
            pending_amount = sum(
                rec.sale_order_line_ids.filtered(lambda line: line.invoice_status != 'invoiced').mapped(
                    'price_total'))
            rec.pending_amount = pending_amount

    @api.depends('appointment_id')
    def _compute_sale_order_count(self):
        for rec in self:
            sale_order_count = self.env['sale.order'].search_count([('appointment_id', '=', rec.id)])
            rec.sale_order_count = sale_order_count

    # def _compute_sale_order_count(self):
    #     for record in self:
    #         record.sale_order_count = self.env['sale.order.line'].search_count(
    #             [('order_id', '=', self.id)])

    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for appointment in self:
            appointment.invoice_count = len(appointment.invoice_ids)

    # @api.depends('sale_order_line_ids.invoice_status')
    # def _compute_invoice_count(self):
    #     for rec in self:
    #         rec.invoice_count = len(
    #             rec.sale_order_line_ids.filtered(lambda line: line.invoice_status == 'invoiced'))

    @api.depends('sale_order_line_ids.is_downpayment')
    def _compute_payment_count(self):
        for rec in self:
            rec.payment_count = len(rec.sale_order_line_ids.mapped('is_downpayment'))

    def action_sale_order(self):
        self.ensure_one()  # Tek bir kayıt için çalıştığından emin olun.
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Sale Orders',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('appointment_id', '=', self.id)],
            'context': {'default_appointment_id': self.id},
        }
        return action
        # for appointment in self:
        #     patient_name = appointment.patient_id.full_name if appointment.patient_id else ''
        #     customer_values = {
        #         'name': f"{patient_name}",
        #         # Diğer gerekli müşteri bilgilerini burada ekleyin
        #     }
        #     customer = self.env['res.partner'].create(customer_values)
        #
        #     sale_order_values = {
        #         'partner_id': customer.id,
        #         # 'partner_id', '=', appointment.patient_id.id,
        #         'date_order': appointment.appointment_date_time,
        #         'note': 'Appointment Patient: %s' % customer.name,
        #         # Diğer gerekli bilgileri burada ekleyin
        #     }
        #     print("Sale Order Oluşturuldu")
        #
        #     sale_order = self.env['sale.order'].create(sale_order_values)
        #
        #     # Satış siparişini düzenleme
        #     self.env.context = dict(self.env.context, default_sale_order_id=sale_order.id)
        #     return {
        #         'name': 'Sale Order',
        #         'type': 'ir.actions.act_window',
        #         'res_model': 'sale.order',
        #         'res_id': sale_order.id,
        #         'view_mode': 'form',
        #         'target': 'current',
        #     }

    def action_invoice(self):
        self.ensure_one()  # Tek bir kayıt için çalıştığından emin olun.

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('appointment_id', '=', self.id)],
            'context': {'default_appointment_id': self.id},
        }

    def action_payment(self):
        for appointment in self:
            # Hasta (patient) veya müşteri (customer) kaydı oluşturun (örnek olarak)

            patient_name = appointment.patient_id.full_name if appointment.patient_id else ''
            customer_values = {
                'name': f"{patient_name}",
                # Diğer gerekli müşteri bilgilerini burada ekleyin
            }
            customer = self.env['res.partner'].create(customer_values)

            # Ödeme (payment) kaydı oluşturun
            payment_values = {
                'partner_id': customer.id,  # Oluşturulan müşteri kaydının ID'sini kullanın
                # 'payment_date': fields.Date.today(),
                # Diğer gerekli ödeme (payment) bilgilerini burada ekleyin
            }
            payment = self.env['account.payment'].create(payment_values)

            # Ödeme (payment) kaydı formunu açın
            self.env.context = dict(self.env.context, default_payment_id=payment.id)
            return {
                'name': 'Payment',
                'type': 'ir.actions.act_window',
                'res_model': 'account.payment',
                'res_id': payment.id,
                'view_mode': 'form',
                'target': 'current',
            }
        # for appointment in self:
        #     payment_values = {
        #         'partner_id': appointment.patient_id.id,
        #         # 'date_order': appointment.appointment_date_time,
        #     }
        #     print("Payment Oluşturuldu")
        #
        #     payment = self.env['account.payment'].create(payment_values)
        #
        #     # Ödeme düzenleme
        #     self.env.context = dict(self.env.context, default_payment_id=payment.id)
        #     return {
        #         'name': 'Payment',
        #         'type': 'ir.actions.act_window',
        #         'res_model': 'account.payment',
        #         'res_id': payment.id,
        #         'view_mode': 'form',
        #         'target': 'current',
        #     }


class AppointmentPrescriptionLines(models.Model):
    _name = "appointment.prescription.lines"
    _description = "Appointment Prescription Lines"

    name = fields.Char(string="Medicine", required=True)
    qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
