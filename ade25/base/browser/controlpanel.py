# -*- coding: utf-8 -*-
"""Control panel for managing basic site settings"""
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface

from ade25.base import MessageFactory as _


class IAde25BaseControlPanel(Interface):

    lqip_enabled = schema.Bool(
        title=_(u"Enable LQIP Support"),
        description=_(u"Activate low quality image placeholder (LQIP) "
                      u"generation in responsive image tool."),
        default=True,
        required=False,
    )


class Ade25BaseControlPanelForm(RegistryEditForm):
    schema = IAde25BaseControlPanel
    schema_prefix = "ade25.base"
    label = u'Ade25 Base Site Settings'


Ade25BaseControlPanelView = layout.wrap_form(
    Ade25BaseControlPanelForm,
    ControlPanelFormWrapper
)
