# -*- coding: utf-8 -*-
"""Module providing utility functions"""
import os
import json
from string import Template

from Products.CMFCore.interfaces import ISiteRoot
from cryptography.fernet import Fernet
from plone import api
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from ade25.base import MessageFactory as _


def get_filesystem_template(name, path, data=dict()):
    template_file = os.path.join(
        path,
        'templates',
        name
    )
    template = Template(open(template_file).read())
    composed = template.substitute(data)
    return composed


def encrypt_data_stream(data):
    """ Encrypt data stream with cryptographic key hashing

    @param data: data string to be encrypted
    @return: dictionary containing the generated encryption key and the
    cryptographically signed data and
    """
    key = Fernet.generate_key()
    f = Fernet(key)
    token = f.encrypt(data)
    return {key: token}


def decrypt_data_stream(key, token):
    """ Decrypt data stream

    @param key: secret encryption key
    @param token: cryptographically signed data
    @return: data string
    """
    f = Fernet(key)
    stream = f.decrypt(token)
    return stream


# TODO: move to config
def default_image_scales():
    available_scales = (
        'default',
        'custom',
        'ratio23',
        'ratio32',
        'ratio34',
        'ratio43',
        'ratio169'
    )
    image_scales = list()
    for scale_name in available_scales:
        scale_info_template = 'image-sizes-{0}.json'.format(scale_name)
        scale_info = get_filesystem_template(
            scale_info_template,
            os.path.dirname(__file__)
        )
        try:
            scale_info_json = json.loads(scale_info)
            image_scales.append(json.dumps(scale_info_json))
        except ValueError:
            pass
    return image_scales


# TODO: move to config
def available_cc_positions():
    position_choices = SimpleVocabulary(
        [SimpleTerm(value=u'top', title=_(u'Top')),
         SimpleTerm(value=u'bottom', title=_(u'Bottom'))]
    )
    return position_choices


def get_acquisition_chain(context_object):
    """
    @return: List of objects from context, its parents to the portal root

    Example::

        chain = getAcquisitionChain(self.context)
        print "I will look up objects:" + str(list(chain))

    @param context_object: Any content object
    @return: Iterable of all parents from the direct parent to the site root
    """

    # It is important to use inner to bootstrap the traverse,
    # or otherwise we might get surprising parents
    # E.g. the context of the view has the view as the parent
    # unless inner is used
    inner = context_object.aq_inner

    content_node = inner

    while content_node is not None:
        yield content_node

        if ISiteRoot.providedBy(content_node):
            break
        if not hasattr(content_node, "aq_parent"):
            raise RuntimeError(
                "Parent traversing interrupted by object: {}".format(
                    str(content_node)
                )
            )
        content_node = content_node.aq_parent


def package_image_scales(package_scales, package_directory):
    image_scales = list()
    for scale_name in package_scales:
        scale_info_template = 'image-sizes-{0}.json'.format(scale_name)
        scale_info = get_filesystem_template(
            scale_info_template,
            package_directory
        )
        try:
            scale_info_json = json.loads(scale_info)
            image_scales.append(json.dumps(scale_info_json))
        except ValueError:
            pass
    return image_scales


def register_image_scales(image_scales):
    """ Run custom add-on package installation code to add custom
       site specific image scales

    """
    registry_settings = api.portal.get_registry_record(
        'ade25.base.responsive_image_scales'
    )
    idx = 0
    for scale in image_scales:
        if scale not in registry_settings:
            registry_settings.append(scale)
            idx += 1
    if idx > 0:
        api.portal.set_registry_record(
            'ade25.base.responsive_image_scales',
            registry_settings
        )
    return image_scales
