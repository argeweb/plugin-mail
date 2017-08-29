#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23
from google.appengine.api.mail_errors import InvalidSenderError

from models.config_model import ConfigModel
from google.appengine.api import app_identity
import weakref

class Mail(object):
    _namespace = None
    _config = None

    def __init__(self, controller):
        self._config = weakref.proxy(ConfigModel.get_by_name('mail_config'))

    @property
    def config(self):
        if self._config is None:
            self._config = weakref.proxy(ConfigModel.get_by_name('mail_config'))
        return self._config

    def send(self, send_to, subject, content=None):
        message = u''
        if send_to is None:
            send_to = u",".join([self.config.system_recipient_1, self.config.system_recipient_2, self.config.system_recipient_3, self.config.system_recipient_4])
        if self.config.use == 0:
            message = self.send_by_google_app_engine(send_to, subject, content)
        if self.config.use == 1:
            message = self.send_by_mail_gun(send_to, subject, content)
        return {'status': 'success', 'message': message}

    def send_width_template(self, template_name, send_to=None, data=None):
        from jinja2 import Template
        from models.mail_model import MailModel
        t = MailModel.get_by_name(template_name)
        if t is None:
            return {'status': 'failure', 'message': u'郵件樣板不存在，無法寄送'}
        subject = Template(t.mail_title).render(data)
        html = Template(t.mail_content).render(data)
        return self.send(send_to, subject, html)

    def send_by_google_app_engine(self, send_to, subject, html):
        from google.appengine.api import mail
        sender = self.config.gae_sender_mail
        if not sender:
            sender = 'noreply@%s.appspotmail.com' % app_identity.get_application_id()

        try:
            res = mail.send_mail(
                sender=sender,
                to=send_to,
                subject=subject,
                body='',
                html=html,
            )
            return res
        except InvalidSenderError:
            pass

    def send_by_mail_gun(self, send_to, subject, html, config):
        import httplib2
        from urllib import urlencode

        http = httplib2.Http()
        http.add_credentials('api', self.config.mg_api_key)

        url = 'https://api.mailgun.net/v3/{}/messages'.format(self.config.mg_domain)
        data = {
            'from': u'{} <{}>'.format(self.config.mg_sender_name, self.config.mg_sender_mail).encode('utf-8'),
            'to': send_to.encode('utf-8'),
            'subject': subject.encode('utf-8'),
            'html': html.encode('utf-8')
        }

        resp, content = http.request(
            url, 'POST', urlencode(data),
            headers={"Content-Type": "application/x-www-form-urlencoded"})

        if resp.status != 200:
            return 'Mailgun API error: {} {}'.format(resp.status, content)
