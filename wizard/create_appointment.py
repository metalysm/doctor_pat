# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CreateAppointmentWizard(models.TransientModel):
    _name = "create.appointment.wizard"
    _description = "Create Appointment Wizard"

    @api.model
    def default_get(self, fields):
        res = super(CreateAppointmentWizard, self).default_get(fields)
        if self._context.get('active_id'):
            res['patient_id'] = self._context.get('active_id')
        return res

    code = fields.Char(string='Code', required=True)
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    doctor_id = fields.Many2many('hospital.doctor', string="Doctor")

    def action_create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            'code': self.code,
            'doctor_id': [(6, 0, self.doctor_id.ids)],
            'stage': 'draft'
        }
        self.env['hospital.appointment'].create(vals)
        # appointment_rec = self.env['hospital.appointment'].create(vals)
        # return {
        #     'name': _('Appointment'),
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'form',
        #     'res_model': 'hospital.appointment',
        #     'res_id': appointment_rec.id,
        # }

    # def action_view_appointment(self):
    #     # action = self.env.ref('om_hospital.action_hospital_appointment').read()[0]
    #     # action['domain'] = [('patient_id', '=', self.patient_id.id)]
    #     # return action
    #
    #     action = self.env['ir.actions.actions']._for_xml_id("om_hospital.action_hospital_appointment")
    #     action['domain'] = [('patient_id', '=', self.patient_id.id)]
    #     return action
    #
    #     # return {
    #     #     'type': 'ir.actions.act_window',
    #     #     'name': 'Appointments',
    #     #     'res_model': 'hospital.appointment',
    #     #     'view_type': 'form',
    #     #     'domain': [('patient_id', '=', self.patient_id.id)],
    #     #     'view_mode': 'tree,form',
    #     #     'target': 'current',
    #     # }
    #     # return action