# -*- coding: utf-8 -*-
"""Module providing utility functions"""
import os
import json
from string import Template

from cryptography.fernet import Fernet
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
