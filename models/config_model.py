#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/2/23.

from argeweb import BasicConfigModel
from argeweb import Fields


class ConfigModel(BasicConfigModel):
    class Meta:
        tab_pages = [u'系統收件人', u'Google App Engine', u'MailGun',
                     # u'SendGrid', u'other'
                     ]

    title = Fields.HiddenProperty(verbose_name=u'設定名稱', default=u'郵件相關設定')
    use = Fields.IntegerProperty(verbose_name=u'服務類型', default=0)

    system_recipient_1 = Fields.StringProperty(verbose_name=u'系統收件人 1', tab_page=0, default=u'example@domain.com')
    system_recipient_2 = Fields.StringProperty(verbose_name=u'系統收件人 2', tab_page=0, default=u'example@domain.com')
    system_recipient_3 = Fields.StringProperty(verbose_name=u'系統收件人 3', tab_page=0, default=u'example@domain.com')
    system_recipient_4 = Fields.StringProperty(verbose_name=u'系統收件人 4', tab_page=0, default=u'example@domain.com')

    gae_sender_mail = Fields.StringProperty(verbose_name=u'寄件者 E-Mail', tab_page=1, default=u'example@domain.com')
    gae_sender_name = Fields.StringProperty(verbose_name=u'寄件者名稱', tab_page=1, default=u'王小華')
    gae_helper = Fields.HtmlProperty(verbose_name=u'說明', tab_page=1, html=u'Google App Engine 每日可寄送 100 封(收件人)，需至 <a href="https://console.cloud.google.com/appengine/settings?project" target="_blank">Google Cloud</a> 設定為 Email API 授權的寄件者。')

    mg_sender_mail = Fields.StringProperty(verbose_name=u'寄件者 E-Mail', tab_page=2, default=u'example@domain.com')
    mg_sender_name = Fields.StringProperty(verbose_name=u'寄件者名稱', tab_page=2, default=u'王小華')
    mg_domain = Fields.StringProperty(verbose_name=u'網域名稱', tab_page=2, default=u'domain.com')
    mg_api_key = Fields.StringProperty(verbose_name=u'Api Key', tab_page=2, default=u'key-as23XVCBDfg43sfgs')
    mg_helper = Fields.HtmlProperty(verbose_name=u'說明', tab_page=2, html=u'Mial Gun 每月可免費寄送 10,000 封信件，請至 <a href="https://www.mailgun.com/" target="_blank">Mial Gun</a> 申請相關 Api Key。')
