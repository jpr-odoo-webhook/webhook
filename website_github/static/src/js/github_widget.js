odoo.define('website_github.githubwidget', function (require) {
"use strict";

var core = require('web.core');
var form_common = require('web.form_common');
var framework = require('web.framework');
var pyeval = require('web.pyeval');
var _t = core._t;



var github_token = form_common.AbstractField.extend({
    template: 'Github_webhookAccess',
    start: function() {
        var self = this;
        this.$el.on('click', 'button.GithubAccess', function() {
            self.allow_github_access();
        });
    },
    allow_github_access: function() {
        var self = this;
        $('button.GithubAccess').prop('disabled', true);
        var context = pyeval.eval('context');
        self.rpc('/website_github/github_access', {
            fromurl: window.location.href,
            local_context: context
        }).done(function(obj) {
            if (obj.status === "need_auth") {
                alert(_t("You will be redirected to Github to authorize access to your Github Account!"));
                framework.redirect(obj.url);
            }
            else if (obj.status === "need_config_from_admin"){
                if (confirm(_t("The Github Application API key needs to be configured before you can use it, do you want to do it now?"))) {
                    self.do_action(obj.action);
                }
            }
        }).always(function() { $('button.GithubAccess').prop('disabled', false); });
    }
});
core.form_widget_registry.add('github_token', github_token);

});