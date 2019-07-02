# -*- coding: utf-8 -*-
"""Module providing embeddable responsive images"""
from Acquisition import aq_inner
from Products.Five import BrowserView
from zope.component import getUtility

from ade25.base.interfaces import IResponsiveImageTool


class ResponsiveImagePreview(BrowserView):
    """ Preview Responsive image template"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def rendered_image(self, field_name='image'):
        context = aq_inner(self.context)
        template = context.restrictedTraverse('@@figure')(
            field_name=field_name
        )
        return template


class ResponsiveImage(BrowserView):
    """ Single responsive image view """

    def __call__(self,
                 image_field_name='image',
                 caption_field_name='caption',
                 scale='default',
                 aspect_ratio='1',
                 lqip=True,
                 lazy_load=True,
                 *args,
                 **kwargs):
        requested_options = {
            'image_field_name': image_field_name,
            'caption_field_name': caption_field_name,
            'scale': scale,
            'aspect_ratio': aspect_ratio,
            'lqip': lqip,
            'lazy_load': lazy_load,
            'uuid': self.context.UID()
        }
        requested_options.update(kwargs)
        self.options = requested_options
        return self.render()

    def render(self):
        return self.index()

    def custom_css_class(self):
        css_class = 'o-figure{}'.format(
            ' ' + self.options.get('css_class', 'o-figure--default')
        )
        return css_class

    def get_image_data(self):
        context = aq_inner(self.context)
        uuid = context.UID()
        tool = getUtility(IResponsiveImageTool)
        image = tool.create(
            self.options
        )
        return image
