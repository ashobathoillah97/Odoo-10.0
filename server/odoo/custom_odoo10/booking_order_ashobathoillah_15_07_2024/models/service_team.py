# -*- coding: utf-8 -*-

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _


class ServiceTeam(models.Model):
    _name = "service.team"
    _description = "Service Team"

    name = fields.Char(string='Team Name', required=True)
    leader_id = fields.Many2one('res.users',string='Team Leader', required=True)
    member_ids = fields.Many2many('res.users','service_team_id',string='Team Member', required=True)


class ResUser(models.Model):
    _inherit = "res.users"

    service_team_id = fields.Many2one('res.users',string='Service')