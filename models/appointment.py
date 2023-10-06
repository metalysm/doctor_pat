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

    _sql_constraints = [
        ('unique_code', 'unique(code)', 'Code must be unique.'),
    ]

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
class AppointmentPrescriptionLines(models.Model):
    _name = "appointment.prescription.lines"
    _description = "Appointment Prescription Lines"

    name = fields.Char(string="Medicine", required=True)
    qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
