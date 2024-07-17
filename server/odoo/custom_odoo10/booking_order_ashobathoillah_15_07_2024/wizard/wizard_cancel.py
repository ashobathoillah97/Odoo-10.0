# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class WorkOrderWizard(models.TransientModel):
    _name = 'work.order.wizard'
    _description = 'Wizard for cancel Work Order'

    reason = fields.Text(string='Reason')
    parent_id = fields.Many2one('work.order',string='Work order')

    def action_cancel_work_order(self):
        if self.parent_id.notes != False:
            self.parent_id.notes = (self.parent_id.notes + self.reason)
        else:
            self.parent_id.notes = self.reason