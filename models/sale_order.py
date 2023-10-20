from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')  # one2many  smart button'da hep bu.
    appointment_ids = fields.One2many('hospital.appointment', 'sale_order_id', string="Appointments")
    # 2.kural ilkte hep tree view açılır sonra form view açılır.
    appointment_count = fields.Integer(string='Appointment', compute='_compute_appointment_count', store=True)
    invoice_count = fields.Integer(string='Invoice', compute='_compute_invoice_count')
    invoice_ids = fields.One2many('account.move', 'appointment_id', compute="_compute_invoice_ids",
                                  store="True")

    @api.depends('appointment_id')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_id) if rec.appointment_id else 0

    def action_open_appointments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointment',
            'view_mode': 'form',
            'res_model': 'hospital.appointment',
            'res_id': self.appointment_id.id,
            'context': {'create': True, 'edit': False},
            'target': 'current',
        }

    # @api.depends('invoice.ids')
    def _compute_invoice_ids(self):
        for rec in self:
            rec.invoice_ids = self.env['account.move'].search([('appointment_id', '=', rec.id)])

    # @api.depends('invoice_ids', 'appointment_id')
    @api.depends('appointment_ids.invoice_ids')
    def _compute_invoice_count(self):
        for order in self:
            invoice_count = sum(len(appointment.invoice_ids) for appointment in order.appointment_ids)
            order.invoice_count = invoice_count
        # for rec in self:
            # invoice_count = self.env['account.move'].search_count([
            #     ('partner_id', '=', rec.partner_id.id),  # Adjust the condition as needed.
            #     ('type_name', '=', 'out_invoice'),  # Use 'out_invoice' for customer invoices.
            # ])
            # rec.invoice_count = invoice_count
            # rec.invoice_count = len(rec.invoice_ids)


    # def action_open_invoice(self):
    #     # Make sure there's only one selected sale order.
    #     # if len(self) != 1:
    #     #     return
    #     #
    #     # # Assuming that you want to create an invoice for the selected sale order.
    #     # sale_order = self
    #     #
    #     # # Create a new invoice based on the sale order.
    #     # invoice_ids = self.env['account.move'].create({
    #     #     'type_name': 'out_invoice',  # Use 'out_invoice' for customer invoices, adjust as needed.
    #     #     'partner_id': sale_order.partner_id.id,
    #     #     'invoice_origin': sale_order.name,
    #     #     'appointment_id': sale_order.appointment_id.id,
    #     #     # You can set other fields for the invoice as needed.
    #     # })
    #     # print('partner id :', sale_order.partner_id.id)
    #     # print('invoice origin :', sale_order.name)
    #     # print('appointment id :', self.appointment_id.id)
    #     #
    #     # # Link the invoice to the sale order (if needed).
    #     # sale_order.write({'invoice_ids': [(4, invoice_ids.id)]})
    #
    #     self.ensure_one()
    #     invoice_ids = self.env['account.move'].search([
    #         ('appointment_id', '=', self.id)
    #     ])
    #     print('invoice id :', invoice_ids)
    #
    #
    #     return {
    #         'name': 'Invoice',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'account.move',
    #         'view_mode': 'tree,form',
    #         # 'res_id': invoice_ids.id,
    #         'domain': [('appointment_id', '=', self.id)],
    #         'target': 'current',
    #     }
        #
        # return action
        # self.ensure_one()
        #
        # domain = [
        #     ('appointment_id', '=', self.appointment_id.id),  # Filter by appointment_id
        #     # You can add more filter conditions if needed
        # ]
        #
        # # Use the search method with the corrected domain
        # invoice_ids = self.env['account.move'].search(domain)
        #
        # # Open the created invoice in form view
        # print('invoice id :', invoice_ids)
        #
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Invoice',
        #     'res_model': 'account.move',
        #     'view_type': 'list,tree,form',
        #     'view_mode': 'list',
        #     'view_id': self.env.ref('account.view_out_invoice_tree').id,
        #     'res_id': invoice_ids.id,
        #     'context': {'create': False, 'edit': False},
        #     'domain': [('appointment_id', '=', self.appointment_id.id)],
        #     'target': 'current',
        # }
    def action_open_invoice(self):
        invoices = self.env['account.move'].search([
            ('appointment_id', '=', self.appointment_id.id),
            # Add other filter conditions if needed
        ])

        # Check if there are invoices and handle accordingly
        if invoices:
            if len(invoices) == 1:
                # If there's only one invoice, open it directly
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Invoice',
                    'res_model': 'account.move',
                    'view_mode': 'form',
                    'res_id': invoices.id,
                    'context': {'create': False, 'edit': False},
                    'target': 'current',
                }
            else:
                # If there are multiple invoices, you can choose to display them in a list view or handle them as needed.
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Invoices',
                    'res_model': 'account.move',
                    'view_type': 'list',
                    'view_mode': 'list,form',
                    'domain': [('id', 'in', invoices.ids)],
                    'context': {'create': False, 'edit': False},
                    'target': 'current',
                }
        else:
            # Handle the case where no invoices were found
            # You can return an informative message or take appropriate action
            return {
                'type': 'ir.actions.act_window',
                'name': 'No Invoices Found',
                'res_model': 'ir.actions.act_window',
                'view_mode': 'form',
                'context': {'create': False, 'edit': False},
                'target': 'current',
                'res_id': self.id,  # Assuming you're returning to the original record
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

    # def action_view_invoice(self):
    #     self.ensure_one()
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Invoices',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'view_id': self.env.ref('account.view_move_form').id,
    #         'res_model': 'account.move',
    #         'domain': [('appointment_id', '=', self.id)],
    #         'context': {'default_appointment_id': self.id},
    #         'target': 'current',
    #     }


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
