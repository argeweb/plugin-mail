#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23.

from argeweb import BasicModel
from argeweb import Fields


class MailConfigModel(BasicModel):
    class Meta:
        tab_pages = [u'系統收件人', u'Google App Engine', u'MailGun', u'SendGrid', u'other']

    name = Fields.StringProperty(verbose_name=u'系統編號')
    title = Fields.StringProperty(default=u'Google App Engine', verbose_name=u'服務名稱')
    use = Fields.IntegerProperty(default=0, verbose_name=u'服務類型')

    system_recipient_1 = Fields.StringProperty(default=u'example@domain.com', verbose_name=u'系統收件人 1', tab_page=0)
    system_recipient_2 = Fields.StringProperty(default=u'example@domain.com', verbose_name=u'系統收件人 2', tab_page=0)
    system_recipient_3 = Fields.StringProperty(default=u'example@domain.com', verbose_name=u'系統收件人 3', tab_page=0)
    system_recipient_4 = Fields.StringProperty(default=u'example@domain.com', verbose_name=u'系統收件人 4', tab_page=0)

    gae_sender_mail = Fields.StringProperty(default=u'example@domain.com', verbose_name=u'寄件者 E-Mail', tab_page=1)
    gae_sender_name = Fields.StringProperty(default=u'王小華', verbose_name=u'寄件者名稱', tab_page=1)

    mg_sender_mail = Fields.StringProperty(default=u'example@domain.com', verbose_name=u'寄件者 E-Mail', tab_page=2)
    mg_sender_name = Fields.StringProperty(default=u'王小華', verbose_name=u'寄件者名稱', tab_page=2)
    mg_domain = Fields.StringProperty(default=u'domain.com', verbose_name=u'網域名稱', tab_page=2)
    mg_api_key = Fields.StringProperty(default=u'key-as23XVCBDfg43sfgs', verbose_name=u'Api Key', tab_page=2)


    @classmethod
    def find_or_create_by_name(cls, name):
        item = cls.find_by_name(name)
        if item is None:
            item = cls()
            item.name = name
            item.put()
        return item