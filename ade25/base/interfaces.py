# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface


class IAde25BaseLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer."""


class IResponsiveImageTool(Interface):
    """ Responsive image generator

        General tool providing srcset compatible image transforms
    """

    def create(self):
        """ Create a set of image scales

        The caller is responsible for passing a valid data dictionary
        containing the necessary details

        Returns dictionary of available scales

        @param uuid:            content object UID (default: context.UID)
        @param image_field:     content object image field (default: image)
        @param image_scale:     predefined image scales set (default: default)
        @param lqip:            opt out from low quality image placeholder
                                support (default: True)
        """


class IContentInfoProvider(Interface):

    def reading_time(self):
        """ Get estimated reading time.
        @return: a time value in minutes
        """

    def time_stamp(self):
        """ Get content time stamp.
        @return: a multipurpose time representation
        """
