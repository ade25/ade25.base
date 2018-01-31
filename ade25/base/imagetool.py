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

    @staticmethod
    def get_origin_scale_info(width, height):
        scale_info = {
            "id": "origin",
            "name": "Origin",
            "size": "origin",
            "width": width,
            "height": height,
            "direction": "keep",
            "quality": "auto"
        }
        return scale_info

    def _get_image_data(self,
                        item,
                        image_field,
                        caption_field,
                        scale,
                        lqip,
                        lazy_load):
        data = {
            'placeholder': IMG,
            'caption': None,
            'lqip': lqip,
            'lazy-load': lazy_load,
        }
        if hasattr(item, caption_field):
            image_caption = getattr(item, caption_field, None)
            data['caption'] = image_caption
        if hasattr(item, image_field):
            srcset = list()
            stored_image = getattr(item, image_field)
            origin_width = stored_image.getImageSize()[0]
            origin_height = stored_image.getImageSize()[1]
            original_scale = self.generate_image(
                item,
                image_field,
                self.get_origin_scale_info(origin_width, origin_height)
            )
            data['origin'] = '{0} {1}w {2}h'.format(
                original_scale['url'],
                original_scale['width'],
                original_scale['height']
            )
            registry_settings = api.portal.get_registry_record(
                'ade25.base.responsive_image_scales'
            )
            registry_set = next((d for i, d in enumerate(registry_settings)
                                 if scale in d), None)
            if registry_set:
                scale_sizes = json.loads(registry_set)
                sizes = scale_sizes[scale]
            else:
                sizes = self.get_default_scale_info()
            for size_info in sizes:
                # Do not attempt to build scales if the original image does
                # not allow for it
                if (
                    (origin_width < int(size_info['width'])) or
                    (origin_height < int(size_info['height']))
                ):
                    continue
                scale_name = size_info['id']
                img = self.generate_image(item, image_field, size_info)
                scale_src = '{0} {1}w {2}h'.format(
                    img['url'], img['width'], img['height']
                )
                data[scale_name] = scale_src
                srcset.append(scale_src)
            placeholder = self.generate_image(
                item, image_field, size_info, generate_lqip=True)
            data['lqip'] = '{0} {1}w {2}h'.format(
                placeholder['url'], placeholder['width'], placeholder['height']
            )
            data['srcset'] = ','.join(str(src) for src in srcset)
        return data

    def generate_image(self,
                       item,
                       image_field,
                       scale_settings,
                       generate_lqip=False):
        """ function used for generating (and potentially storing)
            image scales on demand
        """
        image_scales = getMultiAdapter((item, getRequest()),
                                       name='images')
        settings = scale_settings
        if settings['quality'] == 'auto':
            settings['quality'] = self.get_quality()
        if isinstance(scale_settings['width'], tuple):
            settings['width'] = scale_settings['width'][0]
        if isinstance(scale_settings['height'], tuple):
            settings['height'] = scale_settings['height'][0]
        if hasattr(item, image_field):
            stored_image = getattr(item, image_field)
            if generate_lqip:
                settings['width'] = stored_image.getImageSize()[0]
                settings['height'] = stored_image.getImageSize()[1]
                settings['direction'] = 'keep'
                settings['quality'] = 10
            # Generate scale
            image_scale = image_scales.scale(
                image_field,
                width=int(settings['width']),
                height=int(settings['height']),
                direction=settings['direction'],
                quality=int(settings['quality'])
            )
            image_data = {
                'url': image_scale.url,
                'width': image_scale.width,
                'height': image_scale.height
            }
        else:
            image_data = self.fallback_image_data()
        return image_data
