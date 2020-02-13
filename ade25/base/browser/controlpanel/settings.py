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


class Ade25BaseSettings(BrowserView):
    """ Ade25 settings overview """

    def update(self):
        if super(Ade25BaseSettings, self).update():
            if 'form.button.setup' in self.request.form:
                self.processSetup()

    def processSetup(self):
        IStatusMessage(self.request).addStatusMessage(
            _(u'Setup initialized.'), 'info')


class IAde25BaseControlPanelNavigation(Interface):
    """ Navigation settings """

    display_home_link = schema.Bool(
        title=_(u"Enable Home Link"),
        description=_(u"Choose if the main navigation should include a home "
                      u"link pointing at the front page."),
        default=False,
        required=False
    )

    listed_content_types = schema.List(
        title=_(u"Listed Content Types"),
        value_type=schema.Choice(
            vocabulary='plone.app.vocabularies.ReallyUserFriendlyTypes'
        ),
        default=list(),
        required=False,
    )


class Ade25BaseControlPanelNavigationForm(RegistryEditForm):
    schema = IAde25BaseControlPanelNavigation
    schema_prefix = "ade25.base"
    label = u'Ade25 Responsive Navigation Settings'


Ade25BaseSettingsNavigation = layout.wrap_form(
    Ade25BaseControlPanelNavigationForm,
    ControlPanelFormWrapper
)


class IAde25BaseControlPanelImages(Interface):

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


class Ade25BaseControlPanelImagesForm(RegistryEditForm):
    schema = IAde25BaseControlPanelImages
    schema_prefix = "ade25.base"
    label = u'Ade25 Responsive Image Settings'


Ade25BaseSettingsImages = layout.wrap_form(
    Ade25BaseControlPanelImagesForm,
    ControlPanelFormWrapper
)


class IAde25BaseControlPanelCookieConsent(Interface):

    cc_enabled = schema.Bool(
        title=_(u"Enable Cookie Consent"),
        description=_(u"Activate cookie consent message viewlet"),
        default=False,
        required=False,
    )
    cc_position = schema.Choice(
        title=_(u"CC Popover Position"),
        description=_(u"Please select where to display the cookie consent "
                      u"pop over banner"),
        vocabulary=a25utils.available_cc_positions(),
        required=True,
        default=u'bottom'
    )
    cc_color = schema.TextLine(
        title=_(u"CC Text Color"),
        description=_(u"The entered text color will be used as background "
                      u"color for the popover button"),
        required=False,
    )
    cc_color_bg = schema.TextLine(
        title=_(u"CC Background Color"),
        description=_(u"The entered value will be used as button text color."),
        required=False,
    )
    cc_custom = schema.Bool(
        title=_(u"Override Standard Cookie Consent Text"),
        description=_(u"Activate to use the custom text fields available below."
                      u"Otherwise the default cookie consent message will be "
                      u"automatically rendered which will be appropriate for "
                      u"most sites. The standard cookie message assumes a "
                      u"page to be available under the URI "
                      u"${PORTAL_URL}/datenschutz."),
        default=False,
        required=False,
    )
    cc_message = schema.Text(
        title=_(u"CC Message"),
        description=_(u"Enter custom cookie consent message"),
        default=_(u"This website uses cookies to ensure you get the best "
                  u"experience on our website. Learn more by visiting our "),
        required=False
    )
    cc_link_text = schema.TextLine(
        title=_(u"CC Learn more link text"),
        description=_(u"Enter custom link text for privacy notice"),
        default=_(u"data protection policy."),
        required=False
    )
    cc_link_target = schema.TextLine(
        title=_(u"CC Link Target"),
        description=_(u"Enter relative location of privacy and data "
                      u"protection notice page"),
        default=u'/datenschutzerklaerung',
        required=False
    )
    cc_dismiss_text = schema.TextLine(
        title=_(u"CC Dismiss button"),
        description=_(u"Add custom dismiss button text"),
        default=_(u"Ok"),
        required=False
    )


class Ade25BaseControlPanelCookieConsentForm(RegistryEditForm):
    schema = IAde25BaseControlPanelCookieConsent
    schema_prefix = "ade25.base"
    label = u'Ade25 Cookie Consent Settings'


Ade25BaseSettingsCookieConsent = layout.wrap_form(
    Ade25BaseControlPanelCookieConsentForm,
    ControlPanelFormWrapper
)