# -*- coding: utf-8 -*-
"""Module providing utility functions"""
import os
import json
from string import Template


def get_filesystem_template(name, data=dict()):
    template_file = os.path.join(
        os.path.dirname(__file__),
        'templates',
        name
    )
    template = Template(open(template_file).read())
    composed = template.substitute(data)
    return composed


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
        scale_info = get_filesystem_template(scale_info_template)
        try:
            scale_info_json = json.loads(scale_info)
            image_scales.append(json.dumps(scale_info_json))
        except ValueError:
            pass
    return image_scales
