# -*- coding: utf-8 -*-

from odoo.exceptions import UserError, ValidationError
# from datetime import datetime, timedelta
from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_booking_order = fields.Boolean(string='BO', default=False)
    team_id = fields.Many2one('service.team', string='Team', store=True)
    leader_id = fields.Many2one('res.users', string='Team Leader')
    member_ids = fields.Many2many('res.users', 'sale_order_id', string='Team Member')
    booking_start_date = fields.Datetime('Booking Start')
    booking_end_date = fields.Datetime('Booking End')


    def open_work_order(self):
        return {
            'name': _("Working Orders"),
            'type': 'ir.actions.act_window',
            'view_mode': 'kanban,tree,graph,form,calendar,pivot,graph',
            'res_model': 'work.order',
            'domain': [('booking_order_id', '=', self.id)]
        }

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self.check()
        self._create_work_order()
        return res

    def _create_work_order(self):
        self.env['work.order'].create({
                'wo_number':self.env['ir.sequence'].next_by_code('work.order'),
                'booking_order_id': self.id,
                'planned_start_date': self.booking_start_date,
                'planned_end_date': self.booking_end_date,
                'date_start_date': self.booking_start_date,
                'date_end_date': self.booking_end_date,
                'team_id': self.team_id.id,
                'member_ids': self.member_ids,
                'leader_id': self.leader_id.id,
                'state': 'pending',
            })

    @api.multi
    def check(self):
        sale_order_all = self.env['sale.order'].search([])
        for so in sale_order_all:
            for my_member in self.member_ids:
                if so.leader_id == self.leader_id.id or any(member == my_member for member in so.member_ids):
                    if so.booking_start_date > self.booking_start_date and so.booking_start_date < self.booking_end_date:
                        raise ValidationError('Team already has work order during that period on %s' %self.name)
                    elif so.booking_end_date > self.booking_start_date and so.booking_end_date < self.booking_end_date:
                        raise ValidationError('Team already has work order during that period on %s' %self.name)
        if self.state == 'sale':
            pass
        else:
            raise ValidationError('Team is available for booking')

    @api.onchange('team_id','leader_id')
    def onchange_team_id(self):
        if self.team_id:
            self.update({
                'is_booking_order': True,
                'team_id':self.team_id.id,
                'leader_id': self.team_id.leader_id.id,
                'member_ids': self.team_id.member_ids,
            })

class ResUser(models.Model):
    _inherit = "res.users"

    sale_order_id = fields.Many2one('res.users',string="SO")