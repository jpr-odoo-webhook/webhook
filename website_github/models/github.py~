# -*- coding: utf-8 -*-

from openerp import api, fields, models


class GithubWebhook(models.Model):
    _name = 'github.webhook'

    name = fields.Char(string="Customize Name")
    channel_id = fields.Many2one('mail.channel', string="Channel")
    repository = fields.Char(string="Repository")
    webhook = fields.Char(string="WebHook ID")
