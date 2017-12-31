#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23.
from argeweb import ViewDatastore
from mail import Mail, ConfigModel
from models.mail_model import MailModel
from argeweb.core.events import on


__all__ = (
    'Mail'
    'ConfigModel'
)

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
    }
}


@on('send_mail_width_template')
def send_mail_width_template(controller, template_name, send_to=None, data=None, *args, **kwargs):
    m = Mail(controller)
    return m.send_width_template(template_name=template_name, send_to=send_to, data=data)


@on('send_mail')
def send_mail(controller, subject=None, content=None, send_to=None, *args, **kwargs):
    m = Mail(controller)
    return m.send(subject=subject, content=content, send_to=send_to)


@on('registry_mail_template')
def registry_mail_template(controller, template_name, send_to=None, data=None, *args, **kwargs):
    m = Mail(controller)
    return m.send_width_template(template_name=template_name, send_to=send_to, data=data)


@on('user_request_email_reset')
def user_request_email_reset(controller, *args, **kwargs):
    return event_check(controller, *args, **kwargs)


@on('user_request_verified_email')
def user_request_verified_email(controller, *args, **kwargs):
    return event_check(controller, *args, **kwargs)


@on('after_user_signup')
def after_user_signup(controller, *args, **kwargs):
    return event_check(controller, *args, **kwargs)


@on('after_order_checkout')
def after_order_checkout(controller, order_list, *args, **kwargs):
    return_list = []
    for order in order_list:
        kwargs['order'] = order
        return_list.append(event_check(controller, *args, **kwargs))
    return return_list


@on('after_user_verified_email')
def after_user_verified_email(controller, *args, **kwargs):
    return event_check(controller, *args, **kwargs)


@on('after_user_verified_mobile')
def after_user_verified_mobile(controller, *args, **kwargs):
    return event_check(controller, *args, **kwargs)


@on('after_user_verified_both')
def after_user_verified_both(controller, *args, **kwargs):
    return event_check(controller, *args, **kwargs)


def event_check(controller, *args, **kwargs):
    event_name = kwargs['event_name']
    from google.appengine.api.datastore_errors import BadValueError
    try:
        templates = MailModel.query(MailModel.touch_event==event_name).fetch()
    except BadValueError as e:
        return [{
            'event_name': event_name,
            'message': str(e),
            'status': 'failure'
        }]
    m = Mail(controller)
    return_msg = []
    from datetime import datetime
    kwargs.update({
        'site_name': controller.host_information.site_name,
        'now': controller.util.localize_time(datetime.now()),
        'domain': controller.host_information.host,
    })
    send_to = None
    if 'user' in kwargs:
        send_to = kwargs['user'].email
    if 'send_to' in kwargs:
        send_to = kwargs['send_to']

    for template in templates:
        if template.is_enable:
            if template.send_to_admin:
                send_to_real = 'admin'
            else:
                send_to_real = send_to
            if send_to_real:
                a = m.send_width_template(template=template, send_to=send_to_real, data=kwargs)
                return_msg.append({
                    'mail': template.name,
                    'message': a['message'],
                    'status': a['status']
                })
            else:
                return_msg.append({
                    'mail': template.name,
                    'message': 'no send_to data',
                    'status': 'failure'
                })
    return return_msg
