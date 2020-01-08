# -*- coding: utf-8 -*-
"""Module providing custom navigation strategy"""
from plone import api
from plone.app.layout.viewlets import ViewletBase
from plone.registry.interfaces import IRegistry
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility

from ade25.base import config as ade25_config
from ade25.base.browser.controlpanel import  IAde25BaseControlPanelNavigation


class SiteNavigationViewlet(ViewletBase):
    """ Context aware responsive navigation viewlet """

    index = ViewPageTemplateFile('navigation.pt')

    @property
    def settings(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(
            IAde25BaseControlPanelNavigation,
            prefix='ade25.base')
        return settings

    def section_types(self):
        section_types = list()
        try:
            configured_types = self.settings.listed_content_types
            if configured_types:
                section_types = configured_types
        except KeyError:
            pass
        return section_types

    @property
    def nav_tree_element_close(self):
        try:
            navigation_close = self.settings.navigation_element_close
        except (AttributeError, KeyError):
            navigation_close = ade25_config.navigation_elements(action='close')
        return navigation_close

    def available(self):
        if self.section_types():
            return True
        return False


class SiteTOCViewlet(ViewletBase):
    """ Context aware responsive toc viewlet """

    index = ViewPageTemplateFile('sitemap.pt')

    @property
    def settings(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(
            IAde25BaseControlPanelNavigation,
            prefix='hph.base')
        return settings

    def section_types(self):
        section_types = list()
        try:
            configured_types = self.settings.listed_content_types
            if configured_types:
                section_types = configured_types
            return section_types
        except KeyError:
            return section_types

    def available(self):
        if self.section_types():
            return True
        return False
