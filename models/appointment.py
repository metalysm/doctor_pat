# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"

    appointment_date_time = fields.Datetime(string="Appointment Date & Time")
    code = fields.Char(string="Code", required=True, index=True)
    doctor_id = fields.Many2many(comodel_name='hospital.doctor', string="Doctor", required=True)
    patient_id = fields.Many2one(comodel_name='hospital.patient', string="Patient", required=True)
    stage = fields.Selection([('draft', 'Draft'), ('in-progress', 'In Progress'), ('done', 'Done'),
                              ('cancel', 'Cancel')], default='draft', string="Stage")
    treatment_id = fields.One2many('hospital.treatment', 'appointment_id', string='Treatments')
    prescription = fields.Text(string="Prescription")
    prescription_line_ids = fields.One2many('appointment.prescription.lines', 'appointment_id',
                                            string="Prescription Lines")
    #
    # total_amount = fields.Char(string=' Total Amount', store=True, compute='_compute_total_amount')
    # pending_amount = fields.Char(string=' Pending Amount', store=True, compute='_compute_pending_amount')
    sale_order_line_ids = fields.One2many('sale.order.line', 'order_id', string="Sale Order Lines")
    sale_order_count = fields.Integer(string="Sale Orders", compute="_compute_sale_order_count")
    # invoice_count = fields.Integer(string="Invoices", compute="_compute_invoice_count")
    # payment_count = fields.Integer(string="Payments", compute="_compute_payment_count")

    _sql_constraints = [
        ('unique_code', 'unique(code)', 'Code must be unique.'),
    ]

    #
    #PHASE 1 METHODS
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
        if vals.get('code', _('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        res = super(HospitalAppointment, self).create(vals)
        return res

    def unlink(self):
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

    # @api.depends('sale_order_line_ids')
    # def _compute_total_amount(self):
    #     for rec in self:
    #         total_amount = sum(rec.sale_order_line_ids.mapped('price_total'))
    #         rec.total_amount = total_amount
    #
    # @api.depends('sale_order_line_ids', 'sale_order_line_ids.invoice_status')
    # def _compute_pending_amount(self):
    #     for rec in self:
    #         pending_amount = sum(
    #             rec.sale_order_line_ids.filtered(lambda line: line.invoice_status != 'invoiced').mapped(
    #                 'price_total'))
    #         rec.pending_amount = pending_amount
    #
    @api.depends('sale_order_line_ids.order_id')
    def _compute_sale_order_count(self):
        for rec in self:
            rec.sale_order_count = len(rec.sale_order_line_ids.mapped('order_id'))

    # @api.depends('sale_order_line_ids.invoice_status')
    # def _compute_invoice_count(self):
    #     for rec in self:
    #         rec.invoice_count = len(
    #             rec.sale_order_line_ids.filtered(lambda line: line.invoice_status == 'invoiced'))

    # @api.depends('sale_order_line_ids.payment_ids')
    # def _compute_payment_count(self):
    #     for rec in self:
    #         rec.payment_count = len(rec.sale_order_line_ids.mapped('payment_ids'))
    #
    #

    def action_sale_order(self):
        for appointment in self:
            sale_order_values = {
                'partner_id': appointment.patient_id.id,
                'date_order': appointment.appointment_date_time,
                # Diğer gerekli bilgileri burada ekleyin
            }
            print("Sale Order Oluşturuldu")

            sale_order = self.env['sale.order'].create(sale_order_values)

            # Satış siparişini düzenleme
            self.env.context = dict(self.env.context, default_sale_order_id=sale_order.id)
            return {
                'name': 'Sale Order',
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order',
                'res_id': sale_order.id,
                'view_mode': 'form',
                'target': 'current',
            }


class AppointmentPrescriptionLines(models.Model):
    _name = "appointment.prescription.lines"
    _description = "Appointment Prescription Lines"

    name = fields.Char(string="Medicine", required=True)
    qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
