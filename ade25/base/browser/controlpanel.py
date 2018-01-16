# -*- coding: utf-8 -*-
"""Control panel for managing basic site settings"""
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.protect import CheckAuthenticator
from plone.registry.interfaces import IRegistry
from plone.z3cform import layout
from zope import schema
from zope.component import getUtility
from zope.interface import Interface

from ade25.base import utils as a25utils

from ade25.base import MessageFactory as _


class BaseView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.update()
        if self.request.response.getStatus() not in (301, 302):
            return self.render()
        return ''

    def update(self):
        self.errors = {}

        self.registry = getUtility(IRegistry)
        # self.settings = self.registry.forInterface(ICacheSettings)

        if self.request.method == 'POST':
            CheckAuthenticator(self.request)
            return True
        return False

    def render(self):
        return self.index()


class IAde25BaseControlPanel(Interface):

    lqip_enabled = schema.Bool(
        title=_(u"Enable LQIP Support"),
        description=_(u"Activate low quality image placeholder (LQIP) "
                      u"generation in responsive image tool."),
        default=True,
        required=False,
    )
    responsive_image_scales = schema.List(
        title=_(u"Available Responsive Image Scales"),
        value_type=schema.Text(
            title=_(u"JSON image scale definition")
        ),
        default=a25utils.default_image_scales(),
        required=False,
    )


class Ade25BaseControlPanelForm(RegistryEditForm):
    schema = IAde25BaseControlPanel
    schema_prefix = "ade25base"
    label = u'Ade25 Base Site Settings'


Ade25BaseControlPanelView = layout.wrap_form(
    Ade25BaseControlPanelForm,
    ControlPanelFormWrapper
)


class Ade25BaseSettings(BrowserView):
    """ Ade25 settings overview """

    def update(self):
        import pdb; pdb.set_trace()
        if super(Ade25BaseSettings, self).update():
            if 'form.button.setup' in self.request.form:
                self.processSetup()

    def processSetup(self):
        IStatusMessage(self.request).addStatusMessage(
            _(u'Setup initialized.'), 'info')
