# -*- coding: utf-8 -*-
"""Module providing cookie consent viewlet"""
from plone.app.layout.viewlets import ViewletBase

from plone import api


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
    def position():
        cc_position = api.portal.get_registry_record(
            name='ade25.base.cc_position'
        )
        return cc_position
