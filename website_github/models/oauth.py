# -*- coding: utf-8 -*-

import json as JSON
import urllib
import urllib2


SCOPES = 'user,user:email,user:follow,public_repo,repo,repo_deployment,repo:status,delete_repo,notifications,gist,read:repo_hook,write:repo_hook,admin:repo_hook,admin:org_hook,read:org,write:org,admin:org,read:public_key,write:public_key,admin:public_key'


class Oauth(object):

    def __init__(self, CLIENT_ID, CLIENT_SECRET, from_url='http://www.openerp.com', context=None):
        self.AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
        self.TOKEN_URI = "https://github.com/login/oauth/access_token"
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET
        self.Oauth_Token = None
        self.SCOPES = SCOPES
        self.API_ENDPOINT = "https://api.github.com"
        self.FROM_URL = from_url
        self.CONTEXT = context

    def authorize_github_uri(self):
        data = {
            "client_id": self.CLIENT_ID,
            "redirect_uri": 'http://localhost:8069/website_github/connectd',
            "scope": SCOPES,
        }
        return self.AUTHORIZE_URL + '?' + urllib.urlencode(data)

    def _access_token(self, code):
        data_hook = {
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
            'code': code,
        }
        HTTP_REQUEST = urllib2.Request(self.TOKEN_URI, data=urllib.urlencode(data_hook))
        HTTP_REQUEST.add_header('Accept', 'application/json')
        request_response = urllib2.urlopen(HTTP_REQUEST)
        credentials = JSON.load(request_response)
        return credentials

    def get_all_repos(self, token):
        if token:
            url = ('%s/user/repos') % self.API_ENDPOINT
            HTTP_REQUEST = urllib2.Request(url)
            HTTP_REQUEST.add_header('Accept', 'application/json')
            HTTP_REQUEST.add_header("Authorization", "token %s" % token)
            request_response = urllib2.urlopen(HTTP_REQUEST)
            data = JSON.load(request_response)
            repos_list = []
            user = set()
            for repo in data:
                repos_list.append(repo.get('name'))
                user.add(repo.get('owner')['login'])
            return repos_list, list(user)[0]
        return [], []

    def create_webhook(self, token, value={}):
        if token:
            url = ('%s/repos/%s/%s/hooks') % (self.API_ENDPOINT, value.get('user'), value.get('repos'))
            data = {
                "name": "web",
                "active": 'true',
                "events": ["push", "pull_request"],
                "config": {
                    "url": "http://b329f3a1.ngrok.io/payload",
                }
            }
            HTTP_REQUEST = urllib2.Request(url, data=JSON.dumps(data))
            HTTP_REQUEST.add_header('Accept', 'application/json')
            HTTP_REQUEST.add_header("Authorization", "token %s" % token)
            request_response = urllib2.urlopen(HTTP_REQUEST)
            return JSON.load(request_response), self.FROM_URL
        return {}, self.FROM_URL
