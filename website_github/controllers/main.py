# -*- coding: utf-8 -*-

import json as JSON
from openerp import http
from openerp.http import request
from openerp.addons.website_github.models.oauth import Oauth
import werkzeug.utils


API_ENDPOINT = "https://api.github.com"
AUTH_URI = "https://github.com/login/oauth/authorize"
TOKEN_URI = "https://github.com/login/oauth/access_token"
CLIENT_ID = 'f6ff293a08cd966683a5'
CLIENT_SECRET = 'e882ec4ba5bf069a28e9d015f602287a0a6353c9'
ACCESS_TOKEN = True


class Github(http.Controller):

    @http.route('/payload', methods=['POST'], type='http', auth='public', website=True)
    def payload(self, **kw):

        temp = JSON.loads(kw.get('payload'))
        for key, val in temp.items():
            if temp.get(key) == 'opened':
                print "------------------------->>>", temp['issue']['body']
            elif temp.get(key) == 'created':
                print "------------------------->>>", temp['comment']['body']
        return None

    @http.route('/website_github/github_access', type='json', auth="user")
    def github_authorize(self, **kw):
        #Check if client_id and client_secret are set to get the authorization from Github
        ConfigParameter = request.env['ir.config_parameter']
        request.session['client_id'] = ConfigParameter.get_param('github_client_id', default='')
        request.session['client_secret'] = ConfigParameter.get_param('github_client_secret', default='')
        if not request.session.get('client_id') or not request.session.get('client_secret'):
            request.session['action'] = request.env.ref('base_setup.action_general_configuration').read()[0]
            return {
                "status": "need_config_from_admin",
                "url": '',
                "action": request.session.get('action')
            }
        request.session['aouth'] = Oauth(request.session.get('client_id'), request.session.get('client_secret'), from_url=kw.get('fromurl'), context=kw.get('local_context'))
        url = Oauth.authorize_github_uri(request.session.get('aouth'))
        return {
            "status": "need_auth",
            "url": url
        }

    @http.route('/website_github/connectd', type='http', auth='public', website=True, methods=['POST', 'GET'])
    def github_connected(self, **kw):
        if not kw.get('error') and not request.session.get('access_token'):
            credentials = Oauth._access_token(request.session.get('aouth'), kw['code'])
            request.session['access_token'] = credentials.get('access_token')
        all_repos, request.session['user'] = Oauth.get_all_repos(request.session.get('aouth'), request.session.get('access_token'))
        channel = request.env['mail.channel'].search([])
        return http.request.render('website_github.github_integration_template', {'repos':  all_repos, 'user': request.session.get('user'), 'channel': channel})

    @http.route('/website_github/create/webhook', type='http', auth='public', website=True, methods=['POST'])
    def github_create_webhook(self, **kw):
        Github = request.env['github.webhook']
        temp, url_return = Oauth.create_webhook(request.session.get('aouth'), request.session.get('access_token'), value=kw)
        val = {
            'name': kw.get('name', ''),
            'channel_id': int(kw.get('channel')),
            'repository': kw.get('repos', ''),
            'webhook': temp.get('id')
        }
        Github.create(val)
        return werkzeug.utils.redirect(url_return)
