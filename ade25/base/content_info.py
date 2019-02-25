# -*- coding: utf-8 -*-
"""Module providing reading time adapter"""
from babel.dates import format_datetime
from Acquisition import aq_inner
from plone import api
from plone.dexterity.utils import safe_utf8
from plone.event.utils import pydt
from zope.interface import implementer

from ade25.base.interfaces import IContentInfoProvider


@implementer(IContentInfoProvider)
class ContentInfoProvider(object):

    def __init__(self, context):
        self.context = context

    @staticmethod
    def time_stamp(date_value):
        date = pydt(date_value)
        timestamp = {
            'day': format_datetime(date, 'dd', locale='de'),
            'day_name': format_datetime(date, 'EEEE', locale='de'),
            'month': date.strftime("%m"),
            'month_name': format_datetime(date, 'LLLL', locale='de'),
            'year': date.strftime("%Y"),
            'hour': date.strftime('%H'),
            'minute': date.strftime('%M'),
            'time': format_datetime(date, 'H:mm', locale='de'),
            'date': date,
            'date_short': format_datetime(date, format='short', locale='de'),
            'date_long': format_datetime(date, format='full', locale='de')
        }
        return timestamp

    @staticmethod
    def _readable_text(content_item):
        body = content_item.title + ' ' + content_item.description
        if content_item.text:
            html = content_item.text.raw
            transforms = api.portal.get_tool(name='portal_transforms')
            stream = transforms.convertTo('text/plain',
                                          html,
                                          mimetype='text/html')
            text = stream.getData().strip()
            body = safe_utf8(body) + ' ' + safe_utf8(text)
        return body

    def reading_time(self):
        context = aq_inner(self.context)
        text = self._readable_text(context)
        text_count = len(text.split(' '))
        rt = text_count / 200
        return rt

    def content_snippet(self, characters=320, content_ellipsis='[...]'):
        context = aq_inner(self.context)
        if context.text:
            text = context.text.raw
            portal_transforms = api.portal.get_tool(name="portal_transforms")
            # Output here is a single <p> which contains <br /> for newline
            stream = portal_transforms.convertTo(
                "text/plain", text, mimetype="text/html"
            )
            stream_data = stream.getData().strip()
            cropped_text = context.restrictedTraverse('@@plone').cropText(
                stream_data, characters, content_ellipsis
            )
            return cropped_text
