# -*- coding: utf-8 -*-
"""Init and utils."""

from zope.i18nmessageid import MessageFactory

MessageFactory = MessageFactory('ade25.base')


def initialize(context):
    """Initializer called when used as a product."""
