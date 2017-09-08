# ade25.base

## Ade25: Plone base settings and tools

* `Source code @ GitHub <https://github.com/potzenheimer/ade25.base>`_
* `Releases @ PyPI <http://pypi.python.org/pypi/ade25.base>`_
* `Documentation @ ReadTheDocs <http://ade25base.readthedocs.org>`_
* `Continuous Integration @ Travis-CI <http://travis-ci.org/potzenheimer/ade25.base>`_

## How it works

This package provides a Plone addon as an installable Python egg package.

It includes a set of tools and settings extracted from customer specific
packages due to general need. This package should ideally be included in every
Plone project as a customization starting point.

### Features included

* Base Site Setup (Mail Host settings) (TODO)
* responsive image tool
* installation of dependencies (e.g. `ade25.contentpages)

## Installation

To install `ade25.base` you simply add ``ade25.base``
to the list of eggs in your buildout, run buildout and restart Plone.
Then, install `ade25.base` using the Add-ons control panel.

## TODO

Adopt `IJsonRegistryAware` from **collective.cron** (https://github.com/collective/collective.cron) to actually edit JSON records via the control panel edit form. The implementation would need to add a load and dump function for
actually managing the settings.