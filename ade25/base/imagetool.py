# -*- coding: utf-8 -*-
"""Module providing an image scaling factory."""

from Products.ZCatalog.interfaces import ICatalogBrain
from plone import api
from plone.app.contentlisting.interfaces import IContentListingObject
from plone.scale import scale as image_scale
from zope.component import getMultiAdapter
from zope.globalrequest import getRequest

IMG = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs='


class ResponsiveImagesTool(object):
    """ Factory providing rescaling of project images """

    def create(self, uuid, image_field='image'):
        item = api.content.get(UID=uuid)
        data = self._get_image_data(item, image_field)
        return data

    def _get_image_data(self, item, image_field):
        data = {}
        sizes = ['small', 'medium', 'large', 'original', 'lqip']
        idx = 0
        for size in sizes:
            idx += 0
            img = self._get_scaled_img(item, image_field, size)
            data[size] = '{0} {1}w {2}h'.format(
                img['url'], img['width'], img['height']
            )
        return data

    def _get_scaled_img(self, item, image_field, size):
        request = getRequest()
        if (
                    ICatalogBrain.providedBy(item) or
                    IContentListingObject.providedBy(item)
        ):
            obj = item.getObject()
        else:
            obj = item
        info = {}
        if hasattr(obj, image_field):
            scales = getMultiAdapter((obj, request), name='images')
            if size == 'lgip':
                stored_image = getattr(obj, image_field)
                scale = image_scale.scaleImage(
                    stored_image.data,
                    width=stored_image.getImageSize()[0],
                    height=stored_image.getImageSize()[1],
                    direction='keep',
                    quality=10
                )
            if size == 'small':
                scale = scales.scale(image_field, width=300, height=300)
            if size == 'medium':
                scale = scales.scale(image_field, width=600, height=600)
            if size == 'large':
                scale = scales.scale(image_field, width=900, height=900)
            else:
                scale = scales.scale(image_field, width=1200, height=1200)
            if scale is not None:
                info['url'] = scale.url
                info['width'] = scale.width
                info['height'] = scale.height
            else:
                info['url'] = IMG
                info['width'] = '1px'
                info['height'] = '1px'
        else:
            info['url'] = IMG
            info['width'] = '1px'
            info['height'] = '1px'
        return info
