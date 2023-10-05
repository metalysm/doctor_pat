from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Patient"
    _rec_name = "full_name"

    patient_id = fields.Char(string='Patient Id', readonly=True, store=True, default=lambda self: self.env['ir.sequence'].next_by_code('hospital.patient') or _('New'))
    first_name = fields.Char(string=' First Name')
    last_name = fields.Char(string=' Last Name')
    full_name = fields.Char(string=' Full Name', store=True, compute='_compute_full_name')
    date_of_birth = fields.Date(string="Date of Birth")
    age = fields.Integer(string='Age', readonly=True, compute='_compute_age')
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    national_id_no = fields.Char(string='National Id No', required=True, index=True)

    _sql_constraints = [
        ('unique_national_id_no', 'unique(national_id_no)', 'National ID must be unique.'),
    ]

    # responsible_id = fields.Many2one('res.partner', string="Responsible")
    # appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count')

    def _compute_appointment_count(self):
        for rec in self:
            appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            rec.appointment_count = appointment_count

    @api.onchange('date_of_birth')
    def _compute_age(self):
        for rec in self:
            if rec.date_of_birth:
                rec.age = fields.Date.today().year - rec.date_of_birth.year

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for rec in self:
            rec.full_name = rec.first_name + ' ' + rec.last_name

    # @api.constrains('national_id_no')
    # def _check_unique_national_id_no(self):
    #     for rec in self:
    #         if rec.national_id_no:
    #             existing_patient = self.env['doctor_pat.patient'].search([
    #                 ('national_id_no', '=', rec.national_id_no),
    #                 ('id', '!=', rec.id),
    #             ])
    #             if existing_patient:
    #                 raise ValidationError("National ID No. must be unique.")

    # @api.model
    # def create(self, vals):
    #     if not vals.get('note'):
    #         vals['note'] = 'New Patient'
    #     if vals.get('reference', _('New')) == _('New'):
    #         vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
    #     res = super(HospitalPatient, self).create(vals)
    #     return res

    @api.constrains('name')
    def check_name(self):
        for rec in self:
            patients = self.env['hospital.patient'].search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if patients:
                raise ValidationError(_("Name %s Already Exists" % rec.name))

    @api.constrains('age')
    def check_age(self):
        for rec in self:
            if rec.age == 0:
                raise ValidationError(_("Age Cannot Be Zero .. !"))

    # @api.depends('patient_id')
    # def _compute_patient_id(self):
    #     for rec in self:
    #         patient_id = ''
    #         rec.patient_id = patient_id

    def action_open_appointments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'hospital.appointment',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
            'view_mode': 'tree,form',
            'target': 'current',
        }
