#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23
from models.mail_config_model import MailConfigModel
from google.appengine.api import app_identity
import weakref


class Mail(object):
    _namespace = None
    _config = None

    def __init__(self, controller):
        if hasattr(controller, 'namespace'):
            self._namespace = controller.namespace

    @property
    def config(self):
        if self._config is None:
            self._config = weakref.proxy(MailConfigModel.find_by_name(self._namespace))
        return self._config

    def send(self, send_to, subject, content=None):
        message = u''
        if self.config.use == 0:
            message = Mail.send_by_google_app_engine(send_to, subject, content, self.config)
        if self.config.use == 1:
            message = Mail.send_by_mail_gun(send_to, subject, content, self.config)
        return {'status': 'success', 'message': message}

    def send_width_template(self, template_name, send_to, data=None):
        from jinja2 import Template
        from models.mail_model import MailModel
        t = MailModel.find_by_name(template_name)
        if t is None:
            return {'status': 'failure', 'message': u'郵件樣板不存在，無法寄送'}
        subject = Template(t.mail_title).render(data)
        html = Template(t.mail_content).render(data)
        return self.send(send_to, subject, html)

    @classmethod
    def send_by_google_app_engine(cls, send_to, subject, html, config=None):
        from google.appengine.api import mail
        sender = config.gae_sender_mail
        if not sender:
            sender = 'noreply@%s.appspotmail.com' % app_identity.get_application_id()

        res = mail.send_mail(
            sender=sender,
            to=send_to,
            subject=subject,
            body='',
            html=html,
        )
        return res

    @classmethod
    def send_by_mail_gun(cls, send_to, subject, html, config=None):
        import httplib2
        from urllib import urlencode

        http = httplib2.Http()
        http.add_credentials('api', config.mg_api_key)

        url = 'https://api.mailgun.net/v3/{}/messages'.format(config.mg_domain)
        data = {
            'from': u'{} <{}>'.format(config.mg_sender_name, config.mg_sender_mail).encode('utf-8'),
            'to': send_to.encode('utf-8'),
            'subject': subject.encode('utf-8'),
            'html': html.encode('utf-8')
        }

        resp, content = http.request(
            url, 'POST', urlencode(data),
            headers={"Content-Type": "application/x-www-form-urlencoded"})

        if resp.status != 200:
            return 'Mailgun API error: {} {}'.format(resp.status, content)
