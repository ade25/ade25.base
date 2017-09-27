# -*- coding: utf-8 -*-
"""Module providing an image scaling factory."""
import json
import six

from plone import api
from plone.app.contentlisting.interfaces import IContentListingObject
from plone.scale import scale as image_scaler
from Products.ZCatalog.interfaces import ICatalogBrain
from plone.scale.interfaces import IScaledImageQuality
from zope.component import getMultiAdapter, queryUtility
from zope.globalrequest import getRequest

from ade25.base.utils import get_filesystem_template

IMG = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs='


class ResponsiveImagesTool(object):
    """ Factory providing rescaling of project images """

    def create(self, options):
        item = api.content.get(UID=options['uuid'])
        data = self._get_image_data(
            item,
            options['image_field_name'],
            options['caption_field_name'],
            options['scale'],
            options['lqip'],
            options['lazy_load']
        )
        return data

    @staticmethod
    def fallback_image_data():
        data = {
            'url': IMG,
            'width': '1px',
            'height': '1px',
        }
        return data

    @staticmethod
    def get_quality():
        """Get plone.app.imaging's quality setting"""
        default_scaled_image_quality = queryUtility(IScaledImageQuality)
        if default_scaled_image_quality is None:
            return None
        return default_scaled_image_quality()

    @staticmethod
    def get_default_scale_info():
        scale_info = get_filesystem_template('image-sizes-default.json')
        try:
            info = json.loads(scale_info)
        except ValueError:
            pass
        return info

    def _get_image_data(self,
                        item,
                        image_field,
                        caption_field,
                        scale,
                        lqip,
                        lazy_load):
        data = {}
        registry_settings = api.portal.get_registry_record(
            'ade25base.responsive_image_scales'
        )
        registry_set = next((d for i, d in enumerate(registry_settings)
                             if scale in d), None)
        if registry_set:
            scale_sizes = json.loads(registry_set)
            sizes = scale_sizes[scale]
        else:
            sizes = self.get_default_scale_info()
        for size_info in sizes:
            scale_name = size_info['id']
            img = self.generate_image(item, image_field, size_info)
            data[scale_name] = '{0} {1}w {2}h'.format(
                img['url'], img['width'], img['height']
            )
        placeholder = self.generate_image(
            item, image_field, size_info, generate_lqip=True)
        data['lqip'] = '{0} {1}w {2}h'.format(
            placeholder['url'], placeholder['width'], placeholder['height']
        )
        return data

    def generate_image(self,
                       item,
                       image_field,
                       scale_settings,
                       generate_lqip=False):
        """ function used for generating (and potentially storing)
            image scales on demand
        """
        settings = scale_settings
        if settings['quality'] == 'auto':
            settings['quality'] = self.get_quality()
        if hasattr(item, image_field):
            stored_image = getattr(item, image_field)
            if generate_lqip:
                settings['width'] = stored_image.getImageSize()[0],
                settings['height'] = stored_image.getImageSize()[1],
                settings['direction'] = 'keep',
                settings['quality'] = 10
            # Generate scale
            image_scale = image_scaler.scaleImage(
                stored_image.data,
                width=int(settings['width']),
                height=int(settings['width']),
                direction=settings['direction'],
                quality=int(settings['quality'])
            )
            image_data = {
                'url': image_scale[0],
                'width': image_scale[2][0],
                'height': image_scale[2][1]
            }
        else:
            image_data = self.fallback_image_data()
        return image_data
