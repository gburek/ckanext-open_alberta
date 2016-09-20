from logging import getLogger
import urlparse
import requests
import ckan.logic as logic
import ckan.lib.base as base
import ckan.model as model

from ckan.common import _, request, c
import ckan.lib.helpers as h
import ckan.logic as logic
import ckan.plugins as plugins
import ckan.plugins.toolkit as tk
import ckan.logic.schema as schema
import ckan.lib.navl.dictization_functions as dictization_functions
import ckan.lib.mailer as mailer
from ckan.controllers.user import UserController

from pylons import config
import ckan.lib.captcha as captcha

unflatten = dictization_functions.unflatten


class SuggestController(base.BaseController):

    def __before__(self, action, **env):
        base.BaseController.__before__(self, action, **env)
        try:
            context = {'model': base.model, 'user': base.c.user or base.c.author,
                       'auth_user_obj': base.c.userobj}
            logic.check_access('site_read', context)
        except logic.NotAuthorized:
            base.abort(401, _('Not authorized to see this page'))


    def _send_suggestion(self, context):
        try:
            data_dict = logic.clean_dict(unflatten(
                logic.tuplize_dict(logic.parse_params(request.params))))
            context['message'] = data_dict.get('log_message', '')

            c.form = data_dict['name']
            captcha.check_recaptcha(request)

            #return base.render('suggest/form.html')
        except logic.NotAuthorized:
            base.abort(401, _('Not authorized to see this page'))

        except captcha.CaptchaError:
            error_msg = _(u'Bad Captcha. Please try again.')
            h.flash_error(error_msg)
            return self.suggest_form(data_dict) 


        errors = {}
        error_summary = {}

        if (data_dict["email"] == ''):

            errors['email'] = [u'Missing Value']
            error_summary['email'] =  u'Missing value'

        if (data_dict["name"] == ''):

            errors['name'] = [u'Missing Value']
            error_summary['name'] =  u'Missing value'

        if (data_dict["summary"] == ''):

            errors['summary'] = [u'Missing Value']
            error_summary['summary'] =  u'Missing value'

        if (data_dict["description"] == ''):

            errors['description'] = [u'Missing Value']
            error_summary['description'] =  u'Missing value'


        if len(errors) > 0:
            return self.suggest_form(data_dict, errors, error_summary)
        else:
            # #1799 User has managed to register whilst logged in - warn user
            # they are not re-logged in as new user.
            mail_to = config.get('contact_email_to')
            recipient_name = 'OGP Team'
            subject = 'OGPSuggest - %s' % (data_dict["summary"])

            body = 'Submitted by %s (%s)\n' % (data_dict["name"], data_dict["email"])

            if (data_dict["summary"] != ''):
                body += 'Summary: %s \n' % data_dict["summary"]

            body += 'Request: %s' % data_dict["description"]

            try:
                mailer.mail_recipient(recipient_name, mail_to,
                        subject, body)
            except mailer.MailerException:
                raise


            return base.render('suggest/suggest_success.html')


    def suggest_form(self, data=None, errors=None, error_summary=None):
        suggest_new_form = 'suggest/suggest_form.html'

        context = {'model': base.model, 'session': base.model.Session,
                   'user': base.c.user or base.c.author,
                   'save': 'save' in request.params,
                   'for_view': True}

        if (context['save']) and not data:
            return self._send_suggestion(context)

        data = data or {}
        errors = errors or {}
        error_summary = error_summary or {}
        vars = {'data': data, 'errors': errors, 'error_summary': error_summary}            

        c.form = base.render(suggest_new_form, extra_vars=vars)

        return base.render('suggest/form.html')

    def contact_form(self, data=None, errors=None, error_summary=None):
        contact_new_form = 'suggest/contact_form.html'

        context = {'model': base.model, 'session': base.model.Session,
                   'user': base.c.user or base.c.author,
                   'save': 'save' in request.params,
                   'for_view': True}

        if (context['save']) and not data:
            return self._send_suggestion(context)

        data = data or {}
        errors = errors or {}
        error_summary = error_summary or {}
        vars = {'data': data, 'errors': errors, 'error_summary': error_summary}

        c.form = base.render(contact_new_form, extra_vars=vars)

        return base.render('suggest/form.html')


class PagesController(base.BaseController):

    def __before__(self, action, **env):
        base.BaseController.__before__(self, action, **env)
        try:
            context = {'model': base.model, 'user': base.c.user or base.c.author,
                       'auth_user_obj': base.c.userobj}
            logic.check_access('site_read', context)
        except logic.NotAuthorized:
            base.abort(401, _('Not authorized to see this page'))


    def policy(self):

        return base.render('static-pages/policy/read.html')

    def licence(self):

        return base.render('static-pages/licence/read.html')

    def faq(self):

        return base.render('static-pages/faq/read.html')


class DashboardPackagesController(UserController):
    """This is used to list only user's private data sets"""

    def __before__(self, action, **env):
        UserController.__before__(self, action, **env)
        c.display_private_only = True


from ckan.lib.activity_streams import activity_stream_string_functions, activity_stream_string_icons

activity_stream_string_functions['package reviewed'] = lambda(ctx,activity): tk._("{dataset} has been reviewed")
activity_stream_string_functions['review package'] = lambda(ctx,activity): tk._("{dataset} is due for review")
activity_stream_string_icons['review package'] = 'calendar'


class MonkeyController(base.BaseController):
    def foo(self, id):
        logger = getLogger(__name__)
        ctx = {'user': c.user }
        data = { 'id': id }
        pkg = tk.get_action('package_show')(ctx, data)
        if pkg is None:
            plugins.abort(404, 'No such DS')
        objid = pkg['id']
        from ckan.model import Activity, ActivityDetail
        a = Activity(user_id=c.userobj.id, object_id=objid, revision_id=pkg['revision_id'],
                     activity_type='package needs review', data={'package': pkg})
        a.save()

        return "ok"
