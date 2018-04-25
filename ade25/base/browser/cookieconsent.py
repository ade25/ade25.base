# -*- coding: utf-8 -*-
"""Module providing cookie consent viewlet"""
from Acquisition import aq_inner
from plone import api
from plone.app.layout.viewlets import ViewletBase


class CookieConsentViewlet(ViewletBase):
    """ Context aware responsive navigation viewlet """

    @staticmethod
    def enabled():
        enabled = api.portal.get_registry_record(
            name='ade25.base.cc_enabled'
        )
        if enabled:
            return enabled
        return False

    @staticmethod
    def fallback_messages():
        info_text = (u"In order to optimize our website for you and to be "
                     u"able to continuously improve it, we use cookies. By "
                     u"continuing to use the website, you agree to the use of "
                     u"cookies. Further information on cookies can be found "
                     u"in our")
        link_text = u"privacy policy"
        dismiss_text = u"I understand"
        messages = {
            'message': api.portal.translate(
                info_text,
                'ade25.base',
                api.portal.get_current_language()
            ),
            'link_text': api.portal.translate(
                link_text,
                'ade25.base',
                api.portal.get_current_language()
            ),
            'dismiss_text': api.portal.translate(
                dismiss_text,
                'ade25.base',
                api.portal.get_current_language()
            ),
        }
        return messages

    def _get_registry_settings(self):
        options = [
            'position', 'color', 'color_bg', 'custom',
            'message', 'link_text', 'link_target', 'dismiss_text'
        ]
        settings = {'enabled': self.enabled()}
        for option in options:
            settings[option] = api.portal.get_registry_record(
                name='ade25.base.cc_{0}'.format(option)
            )
        return settings

    def settings(self):
        context = aq_inner(self.context)
        settings = self._get_registry_settings()
        fallback = self.fallback_messages()
        if not settings['custom']:
            settings['message'] = fallback['message']
            settings['link_text'] = fallback['link_text']
            settings['dismiss_text'] = fallback['dismiss_text']
            settings['link_target'] = context.absolute_url()
        return settings

