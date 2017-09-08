# -*- coding: utf-8 -*-
"""Module providing utility functions"""
import os
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
