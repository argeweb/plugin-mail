#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23
from google.appengine.api.mail_errors import InvalidSenderError
from jinja2 import TemplateSyntaxError, UndefinedError

from models.config_model import ConfigModel
from google.appengine.api import app_identity
import weakref


class Mail(object):
    _namespace = None
    _config = None

    def __init__(self, controller=None, config=None):
        if config is None:
            self._config = weakref.proxy(ConfigModel.get_config())
        else:
            self._config = config

    @property
    def config(self):
        if self._config is None:
            self._config = weakref.proxy(ConfigModel.get_config())
        return self._config

    def send(self, send_to, subject, content=None, cc=''):
        if send_to is 'admin':
            send_to = u",".join([self.config.system_recipient_1, self.config.system_recipient_2, self.config.system_recipient_3, self.config.system_recipient_4])
        try:
            if self.config.use == 0:
                return self.send_by_google_app_engine(send_to, subject, content, cc)
            if self.config.use == 1:
                return self.send_by_mail_gun(send_to, subject, content, cc)
        except Exception as e:
            return {'status': 'failure', 'message': str(e)}

    def send_width_template(self, template=None, template_name=None, send_to=None, data=None):
        from jinja2 import Template
        from models.mail_model import MailModel
        if template is None and template_name and isinstance(template_name, str):
            template = MailModel.get_by_name(template_name)
        if template is None:
            return {'status': 'failure', 'message': u'郵件樣板不存在，無法寄送 (not exist)'}
        if template.is_enable:
            if template.send_to_admin:
                send_to_real = 'admin'
            else:
                send_to_real = send_to
        else:
            return {'status': 'failure', 'message': u'郵件樣板未啟用，無法寄送 (disable)'}
        if send_to_real is None:
            return {'status': 'failure', 'message': u'缺少寄送的目標，無法寄送 (not target)'}
        try:
            subject = Template(template.mail_title).render(data)
            html = Template(template.mail_content).render(data)
            return self.send(send_to_real, subject, html)
        except Exception as e:
            import logging
            logging.error(template.mail_title)
            logging.error(str(e))
            return {'status': 'failure', 'message': u'郵件樣板設定錯誤，無法寄送 (config error)'}

    def send_by_google_app_engine(self, send_to, subject, html, cc):
        from google.appengine.api import mail
        sender = self.config.gae_sender_mail
        if not sender:
            sender = 'noreply@%s.appspotmail.com' % app_identity.get_application_id()

        import logging
        logging.info(html)
        try:
            res = mail.send_mail(
                sender=sender,
                to=send_to,
                subject=subject,
                body='',
                html=html,
            )
            from .models.mail_record_model import MailRecordModel
            mr = MailRecordModel()
            mr.title = subject
            mr.send_to = send_to
            mr.content = html
            mr.sender = sender
            mr.send_system = 'Google App Engine'
            mr.put()
            return {'status': 'success', 'message': u'信件已寄出'}
        except InvalidSenderError as e:
            return {'status': 'failure', 'message': str(e)}
        except:
            return {'status': 'failure', 'message': u'寄送失敗'}

    def send_by_mail_gun(self, send_to, subject, html, cc):
        import httplib2
        from urllib import urlencode

        http = httplib2.Http()
        http.add_credentials('api', self.config.mg_api_key)

        url = 'https://api.mailgun.net/v3/{}/messages'.format(self.config.mg_domain)
        import logging
        logging.info(html)

        data = {
            'from': u'{} <{}>'.format(self.config.mg_sender_name, self.config.mg_sender_mail).encode('utf-8'),
            'to': send_to.encode('utf-8'),
            'subject': subject.encode('utf-8'),
            'html': html.encode('utf-8')
        }
        if cc and cc is not u'':
            data['cc'] = cc

        resp, content = http.request(
            url, 'POST', urlencode(data),
            headers={"Content-Type": "application/x-www-form-urlencoded"})

        if resp.status != 200:
            return {'status': 'failure', 'message': 'Mailgun API error: {} {}'.format(resp.status, content)}
        return {'status': 'success', 'message': u'信件已寄出'}
