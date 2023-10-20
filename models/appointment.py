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

    total_amount = fields.Float(string="Total Amount", compute="_compute_total_amount", store=True)
    pending_amount = fields.Char(string=' Pending Amount', store=True, compute='_compute_pending_amount')

    sale_order_line_ids = fields.One2many('sale.order.line', 'appointment_id', string="Sale Order Line")
    sale_order_count = fields.Integer(string="Sale Orders", compute="_compute_sale_order_count")
    sale_order_id = fields.Many2one(comodel_name="sale.order", string="Sale Order")
    invoice_ids = fields.One2many('account.move', 'appointment_id', string='Invoice', compute='_compute_invoice_ids')
    account_move_id = fields.Many2one('account.move')
    payment_ids = fields.One2many('account.payment', 'appointment_id', string='Payment', compute='_compute_payment_ids')
    account_payment_id = fields.Many2one('account.payment')
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer")
        # required=True, readonly=False, change_default=True, index=True,
        # tracking=1,)

    invoice_count = fields.Integer(string='Invoice Count', compute='_compute_invoice_count')
    payment_count = fields.Integer(string="Payment Count", compute="_compute_payment_count")

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

    @api.model
    def create(self, vals):
        print("Appointment create vals ", vals)
        vals['code'] = self.env['ir.sequence'].next_by_code("hospital.appointment")
        return super(HospitalAppointment, self).create(vals)

    def unlink(self):  # for undeletable done states
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

    @api.depends('invoice_ids')
    def _compute_invoice_ids(self):
        for rec in self:
            rec.invoice_ids = self.env['account.move'].search([('appointment_id', '=', rec.id)])

    @api.depends('payment_ids')
    def _compute_payment_ids(self):
        for rec in self:
            rec.payment_ids = self.env['account.payment'].search([('appointment_id', '=', rec.id)])

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

    @api.depends('sale_order_line_ids')
    def _compute_sale_order_count(self):
        for rec in self:
            sale_order_count = self.env['sale.order'].search_count([('appointment_id', '=', self.id)])
            rec.sale_order_count = sale_order_count

    # @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        for rec in self:
            # invoice_count = self.env['account.move'].search_count([
            #     ('appointment_id', '=', rec.id)
            #     # Add your search criteria here.
            # ])
            rec.invoice_count = len(rec.invoice_ids)

    # @api.depends('sale_order_line_ids.payment_ids')
    # @api.depends('payment_ids')
    def _compute_payment_count(self):
        for rec in self:
            payment_count = self.env['account.payment'].search_count([
                ('appointment_id', '=', rec.id)
            ])
            rec.payment_count = payment_count
            # payment_count = len(rec.payment_ids)
            # rec.payment_count = payment_count

    def action_sale_order(self):
        # self.ensure_one()  # Tek bir kayıt için çalıştığından emin olun.
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Sale Orders',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('appointment_id', '=', self.id)],  # filtered
            'context': {'default_appointment_id': self.id},  # setting default appointment
        }
        return action

    def action_sale_order_create(self):
        self.ensure_one()  # Tek bir kayıt için çalıştığından emin olun.
        self.partner_id = self.env['res.partner'].create({
            'name': self.patient_id.full_name,
            'mobile': self.patient_id.phone,
            'email': self.patient_id.email,
        })


        sale_order_values = {
            'partner_id': self.partner_id.id,
            'appointment_id': self.id,
            'order_line': []
        }

        sale_order = self.env['sale.order'].create(sale_order_values)
        order_line_id = self.env['sale.order.line'].create({
            'product_id': self.env['product.product'].search([('id', '=', 4)]).id,
            'order_id': sale_order.id,
        })
        print('sale order: ', sale_order.name)
        print('partner id : ', sale_order.partner_id.name)

        self.sale_order_id = sale_order.id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Orders',
            'res_model': 'sale.order',
            'res_id': sale_order.id,
            'view_mode': 'form',
            # 'domain': [('appointment_id', '=', self.id)],  # filtered  # akıllı buton için
            # 'context': {'default_appointment_id': self.id},  # setting default appointment
            'target': 'current'
        }

    def action_invoice(self):
        # self.ensure_one()
        invoice_ids = self.env['account.move'].search([
            ('appointment_id', '=', self.id)
        ])
        print('invoice id :', invoice_ids)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            # 'res_id': invoice_ids.id, #create olsaydı kullanılırdı.
            'view_mode': 'tree,form',
            'target': 'current',
            # 'type': 'ir.actions.act_window',
            # 'name': 'Invoices',
            # 'view_type': 'tree,form',
            # 'view_mode': 'form',
            # # 'view_id': self.env.ref('account.view_move_form').id,
            # 'res_model': 'account.move',
            'domain': [('appointment_id', '=', self.id)],
            #'domain': [('id', 'in', invoice_ids.ids)]
            # 'context': {'default_appointment_id': self.id},
            # # 'context': "{'type':'out_invoice'}",
            # 'target': 'current',
        }

    def action_payment(self):
        # self.ensure_one()
        # payment_ids = self.env['account.payment'].search([
        #     ('appointment_id', '=', self.id)
        # ])
        #
        # print('payment id: ', payment_ids)
        # # for appointment in self:
        # #     # Hasta (patient) veya müşteri (customer) kaydı oluşturun (örnek olarak)
        # #
        # #     patient_name = appointment.patient_id.full_name if appointment.patient_id else ''
        # #     customer_values = {
        # #         'name': f"{patient_name}",
        # #         # Diğer gerekli müşteri bilgilerini burada ekleyin
        # #     }
        # #     customer = self.env['res.partner'].create(customer_values)
        # #
        # #     # Ödeme (payment) kaydı oluşturun
        # #     payment_values = {
        # #         'partner_id': customer.id,  # Oluşturulan müşteri kaydının ID'sini kullanın
        # #         # 'payment_date': fields.Date.today(),
        # #         # Diğer gerekli ödeme (payment) bilgilerini burada ekleyin
        # #     }
        # #     payment = self.env['account.payment'].create(payment_values)
        # #
        # #     # Ödeme (payment) kaydı formunu açın
        # #     self.env.context = dict(self.env.context, default_payment_id=payment.id)
        # return {
        #     'name': 'Payment',
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'account.payment',
        #     # 'res_id': payment_ids.id,
        #     'view_mode': 'tree,form',
        #     'target': 'current',
        #     'domain': ['appointment_id', '=', self.id],
        # }
        # self.ensure_one()  # Ensure you're working with a single record.
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payments',
            'res_model': 'account.payment',
            'view_mode': 'tree,form',
            'domain': [('appointment_id', '=', self.id)],  # Filter by appointment
            'context': {'default_appointment_id': self.id},  # Set the default appointment
            'stage': 'posted',
        }


class AppointmentPrescriptionLines(models.Model):
    _name = "appointment.prescription.lines"
    _description = "Appointment Prescription Lines"

    name = fields.Char(string="Medicine", required=True)
    qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
