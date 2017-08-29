#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23.

from argeweb import ViewDatastore
from mail import Mail, ConfigModel
from argeweb.core.events import on


__all__ = (
    'Mail'
    'ConfigModel'
)


@on('send_mail_width_template')
def send_mail_width_template(controller, template_name, send_to=None, data=None):
    m = Mail(controller)
    m.send_width_template(template_name=template_name, send_to=send_to, data=data)


@on('registry_mail_template')
def registry_mail_template(controller, template_name, send_to=None, data=None):
    m = Mail(controller)
    m.send_width_template(template_name=template_name, send_to=send_to, data=data)

plugins_helper = {
    'title': u'郵件樣版與寄送設定',
    'desc': u'與郵件有關的相關設定，並可建立郵件樣版',
    'controllers': {
        'mail': {
            'group': u'郵件樣版管理',
            'actions': [
                {'action': 'list', 'name': u'郵件樣版'},
                {'action': 'add', 'name': u'新增樣版'},
                {'action': 'edit', 'name': u'編輯樣版'},
                {'action': 'view', 'name': u'檢視樣版'},
                {'action': 'delete', 'name': u'刪除樣版'},
                {'action': 'plugins_check', 'name': u'啟用停用模組'},
            ]
        },
        'config': {
            'group': u'郵件設定',
            'actions': [
                {'action': 'config', 'name': u'郵件相關設定'},
            ]
        },
    },
    'install_uri': 'mail:config:after_install'
}
