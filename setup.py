# -*- coding: utf-8 -*-
"""Installer for the ade25.base package."""

from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = read('README.rst')

setup(
    name='ade25.base',
    version='1.0.0',
    description="Ade25: Plone base settings and tools",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='Plone, Python, Utilities',
    author='Christoph Boehner-Figas',
    author_email='cb@ade25.de',
    url='http://pypi.python.org/pypi/ade25.base',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['ade25'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'babel',
        'html2text',
        'setuptools',
        'plone.app.dexterity [relations]',
        'plone.app.relationfield',
        'plone.namedfile [blobs]',
    ],
    extras_require={
        'test': [
            'mock',
            'plone.app.testing',
            'unittest2',
        ],
        'develop': [
            'coverage',
            'flake8',
            'jarn.mkrelease',
            'plone.app.debugtoolbar',
            'plone.reload',
            'Products.Clouseau',
            'Products.DocFinderTab',
            'Products.PDBDebugMode',
            'Products.PrintingMailHost',
            'Sphinx',
            'zest.releaser',
            'zptlint',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
