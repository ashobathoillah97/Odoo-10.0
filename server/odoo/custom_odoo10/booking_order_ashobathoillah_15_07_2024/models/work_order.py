# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _

view_mode = [
    ('pending', 'Pending'),
    ('in_progress', 'In Progress'),
    ('done', 'Done'),
    ('cancel', 'Cancelled'),
]

class WorkOrder(models.Model):
    _name = "work.order"
    _description = "Work Order"

    wo_number = fields.Char(string='WO Number', copy=False, store=True)
    booking_order_id = fields.Many2one('sale.order',string='BO Ref', readonly=True)
    team_id = fields.Many2one('service.team', string='Team', store=True)
    leader_id = fields.Many2one('res.users', string='Team Leader')
    member_ids = fields.Many2many('res.users', 'work_order_id', string='Team Member')
    planned_start_date = fields.Datetime('Planned Start', required=True)
    planned_end_date = fields.Datetime('Planned End', required=True)
    date_start_date = fields.Datetime('Date Start', readonly=True)
    date_end_date = fields.Datetime('Date End', readonly=True)
    state = fields.Selection(view_mode, string='View Type', required=True)
    notes = fields.Text(string='Notes')

    def action_start_work(self):
        self.state = 'in_progress'

    def action_cancel(self):
        self.state = 'cancel'

    def action_reset(self):
        self.state = 'pending'
        self.date_start_date = False

    def action_end_work(self):
        self.state = 'done'
        self.date_end_date = datetime.now()

    @api.onchange('team_id')
    def onchange_team_id(self):
        if self.team_id:
            members = []
            for x in self.team_id.member_ids:
                members.append(x.id)
            self.update({
                'leader_id': self.team_id.leader_id.id,
                'member_ids': self.team_id.member_ids,
            })

    @api.model
    def create(self, vals):
        # raise ValidationError(vals)
        res = super(WorkOrder, self).create(vals)
        return res

class ResUser(models.Model):
    _inherit = "res.users"

    work_order_id = fields.Many2one('res.users',string='WO')
