# -*- coding: utf-8 -*-

from openerp import fields, models, api


class GitHubConfigSettings(models.TransientModel):
    _inherit = 'base.config.settings'

    github_sync = fields.Boolean(string="Show tutorial to know how to get my 'Client ID' and my 'Client Secret'")
    github_client_id = fields.Char(string='Client ID')
    github_client_secret = fields.Char(string='Client Secret')
    github_webhook_authorization = fields.Char(string='Github authorization')

    @api.model
    def set_default_github_setting(self, ids):
        params = self.env['ir.config_parameter']
        myself = self.browse(ids[0])
        params.set_param('github_client_id', myself.github_client_id or '', groups=['base.group_system'])
        params.set_param('github_client_secret', myself.github_client_secret or '', groups=['base.group_system'])

    @api.model
    def get_default_github_setting(self, ids):
        params = self.env['ir.config_parameter']
        github_client_id = params.get_param('github_client_id', default='')
        github_client_secret = params.get_param('github_client_secret', default='')
        return {'github_client_id': github_client_id, 'github_client_secret': github_client_secret}
