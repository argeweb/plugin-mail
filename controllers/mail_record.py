#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23.

from argeweb import Controller, scaffold, route_menu, route
from google.appengine.api import app_identity


class MailRecord(Controller):
    class Scaffold:
        hidden_in_form = ['check_time']

    @route
    def admin_add(self):
        if self.request.method == 'POST':
            from ..mail import Mail
            m = Mail(self)

            def send_mail(**kwargs):
                item = kwargs['item']
                s = m.send(item.send_to, item.title, item.content, item.cc)
            self.events.scaffold_after_save += send_mail
            return scaffold.add(self)
        else:
            from ..models.config_model import ConfigModel
            config_record = ConfigModel.get_config()
            self.context['use'] = config_record.use
            query = self.params.get_string('query', u'')
            email = self.params.get_string('email', u'')
            template_name = self.params.get_string('template_name', u'')
            data = self.params.get_dict_from_string('query')
            if query is not '':
                if 'email' in data:
                    email = data['email']
                if 'template_name' in data:
                    template_name = data['template_name']

            scaffold.add(self)
            if template_name is not u'':
                from ..models.mail_model import MailModel
                template = MailModel.get_by_name(template_name)
                if template and template.is_enable:
                    if template.send_to_admin:
                        send_to_real = 'admin'
                    else:
                        send_to_real = email
                    self.context['send_to'] = send_to_real
                    try:
                        from jinja2 import Template
                        self.context['title'] = Template(template.mail_title).render(data)
                        self.context['content'] = Template(template.mail_content).render(data)
                    except:
                        pass
            self.scaffold.change_field_visibility('send_date', False, False)

    @route_menu(list_name=u'system', group=u'郵件寄送', text=u'郵件寄送記錄', sort=704)
    def admin_list(self):
        return scaffold.list(self)
