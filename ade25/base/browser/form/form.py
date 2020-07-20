# -*- coding: utf-8 -*-
"""Module providing form utilities and partials"""
import uuid as uuid_tool
from Acquisition import aq_inner
from Products.Five import BrowserView
from plone import api
from plone.protect.utils import addTokenToUrl


class FormFieldBase(BrowserView):
    """ Default widget view

    Renders the provided template and view by the widget in question
    """
    def __call__(self,
                 field_type='text-line',
                 field_identifier=None,
                 field_name=None,
                 field_help=None,
                 field_data=None,
                 field_error=None,
                 field_required=False,
                 **kw):
        self.params = {
            'field_identifier': field_identifier,
            'field_name': field_name,
            'field_help': field_help,
            'field_type': field_type,
            'field_error': field_error,
            'field_required': field_required,
            'field_data': field_data
        }
        self.params.update(kw)
        return self.render()

    def render(self):
        return self.rendered_widget()

    @property
    def field_configuration(self):
        return self.params['field_data']

    def field_name(self):
        translation_service = api.portal.get_tool(name="translation_service")
        translated_name = translation_service.translate(
            self.params['field_name'],
            'lra.cos',
            target_language=api.portal.get_default_language()
        )
        return translated_name

    def field_css_class(self):
        config = self.field_configuration
        field_error = self.params['field_error']
        base_class = "o-form__field"
        class_list = [base_class, ]
        modifiers = config["css_class_modifier"]
        if self.params['field_type']:
            modifiers.append(self.params['field_type'])
            if self.params['field_type'] in ['boolean', 'privacy']:
                modifiers.append('checkbox')
        if self.params['field_required']:
            modifiers.append("required")
        if field_error and field_error['active'] is True:
            modifiers.append("has-error")
        for modifier in modifiers:
            class_list.append(
                "{0}--{1}".format(base_class, modifier)
            )
        return " ".join(class_list)

    def field_data(self):
        request_data = self.field_configuration
        field_data = dict()
        if request_data:
            field_data = request_data
        return field_data

    def field_extra(self):
        field_extra_data = dict()
        for key, value in self.params.items():
            if not key.startswith('field_'):
                field_extra_data[key] = value
        return field_extra_data

    def rendered_widget(self):
        context = aq_inner(self.context)
        if self.params['field_type']:
            view_name = '@@ade25-base-form-field-{0}'.format(
                self.params['field_type']
            )
            rendered_widget = context.restrictedTraverse(view_name)(
                field_identifier=self.params['field_identifier'],
                field_name=self.field_name(),
                field_help_text=self.params['field_help'],
                field_error=self.params['field_error'],
                field_data=self.field_data(),
                field_css_class=self.field_css_class(),
                field_required=self.params['field_required'],
                field_extra_data=self.field_extra()
            )
        else:
            view_name = '@@ade25-base-form-field-text'
            rendered_widget = context.restrictedTraverse(view_name)(
                field_identifier=self.params['field_identifier'],
                field_name=self.field_name(),
                field_help_text=self.params['field_help'],
                field_data=self.field_data(),
                field_css_class=self.field_css_class(),
                field_required=self.params['field_required'],
                field_extra_data=self.field_extra()
            )
        return rendered_widget


class FormFieldTextLine(BrowserView):

    def __call__(self,
                 field_identifier=None,
                 field_name=None,
                 field_data=None,
                 field_error=None,
                 **kw):
        self.params = {
            'field_identifier': field_identifier,
            'field_name': field_name,
            'field_error': field_error,
            'field_data': field_data
        }
        self.params.update(kw)
        return self.render()

    def settings(self):
        return self.params

    def render(self):
        return self.index()


class FormFieldTextArea(BrowserView):

    def __call__(self,
                 field_identifier=None,
                 field_name=None,
                 field_data=None,
                 field_error=None,
                 **kw):
        self.params = {
            'field_identifier': field_identifier,
            'field_name': field_name,
            'field_error': field_error,
            'field_data': field_data
        }
        self.params.update(kw)
        return self.render()

    def settings(self):
        return self.params

    def render(self):
        return self.index()


class FormFieldSelect(BrowserView):

    def __call__(self,
                 field_identifier=None,
                 field_name=None,
                 field_data=None,
                 field_error=None,
                 **kw):
        self.params = {
            'field_identifier': field_identifier,
            'field_name': field_name,
            'field_error': field_error,
            'field_data': field_data
        }
        self.params.update(kw)
        return self.render()

    def settings(self):
        return self.params

    def render(self):
        return self.index()

    def field_widget_options(self):
        if self.settings()['field_extra_data']:
            if 'widget_options' in self.settings()['field_extra_data']:
                return self.settings()['field_extra_data']['widget_options']
        return None

    def widget_options(self):
        translation_service = api.portal.get_tool(name="translation_service")
        widget_options = dict()
        options = self.field_widget_options()
        for option_name, option_value in options.items():
            widget_options[option_name] = translation_service.translate(
                option_value,
                'lra.cos',
                target_language=api.portal.get_default_language()
            )
        return widget_options


class FormFieldBoolean(BrowserView):

    def __call__(self,
                 field_identifier=None,
                 field_name=None,
                 field_data=None,
                 field_error=None,
                 **kw):
        self.params = {
            'field_identifier': field_identifier,
            'field_name': field_name,
            'field_error': field_error,
            'field_data': field_data
        }
        self.params.update(kw)
        return self.render()

    def settings(self):
        return self.params

    def render(self):
        return self.index()


class FormFieldPrivacy(BrowserView):

    def __call__(self,
                 field_identifier=None,
                 field_name=None,
                 field_data=None,
                 field_error=None,
                 **kw):
        self.params = {
            'field_identifier': field_identifier,
            'field_name': field_name,
            'field_error': field_error,
            'field_data': field_data
        }
        self.params.update(kw)
        return self.render()

    def settings(self):
        return self.params

    def render(self):
        return self.index()

    def widget_action_url(self):
        action_url = "{portal_url}/{privacy_link}".format(
            portal_url=api.portal.get().absolute_url(),
            privacy_link=self.settings()['field_help_text']['help_text_link_url']
        )
        return addTokenToUrl(action_url)
