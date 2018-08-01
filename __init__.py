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
        'mail_record': {
            'group': u'郵件發送記錄',
            'actions': [
                {'action': 'list', 'name': u'郵件發送記錄'},
                {'action': 'add', 'name': u'新增郵件發送記錄'},
                {'action': 'edit', 'name': u'編輯郵件發送記錄'},
                {'action': 'view', 'name': u'檢視郵件發送記錄'},
                {'action': 'delete', 'name': u'刪除郵件發送記錄'},
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
def registry_mail_template(controller, template_name, touch_event=None, title=None, mail_title=None, mail_content=None,
                           is_enable=True, send_to_admin=False, *args, **kwargs):
        record = MailModel.get_or_create_by_name(template_name)
        record.name = template_name
        if title:
            record.title = title
        if mail_title:
            record.mail_title = mail_title
        if mail_content:
            record.mail_content = mail_content
        if touch_event:
            record.touch_event = touch_event
        record.is_enable = is_enable
        record.send_to_admin = send_to_admin
        record.put()
        return {
            'record': record.name,
            'message': u'Mail Template %s is created' % template_name,
            'status': u'success'
        }


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
    if 'user' in kwargs and kwargs['user'] is not None:
        send_to = kwargs['user'].email
    if 'send_to' in kwargs:
        send_to = kwargs['send_to']

    for template in templates:
        a = m.send_width_template(template=template, send_to=send_to, data=kwargs)
        return_msg.append({
            'mail': template.name,
            'message': a['message'],
            'status': a['status']
        })
    return return_msg
