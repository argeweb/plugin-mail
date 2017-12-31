#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23.

from argeweb import Controller, scaffold, route_menu, route
from google.appengine.api import app_identity


class Config(Controller):
    class Scaffold:
        display_in_list = ['is_enable', 'category']
        hidden_in_form = ['name', 'title', 'use']

    @route
    @route_menu(list_name=u'system', group=u'郵件寄送', text=u'郵件相關設定', sort=702)
    def admin_config(self):
        self.context['application_id'] = app_identity.get_application_id()
        self.meta.view.template_name = '/mail/config.html'
        config_record = self.meta.Model.get_config()
        return scaffold.edit(self, config_record.key)
