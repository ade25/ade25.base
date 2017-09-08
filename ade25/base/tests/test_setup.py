# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from ade25.base.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of ade25.base into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if ade25.base is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('ade25.base'))

    def test_uninstall(self):
        """Test if ade25.base is cleanly uninstalled."""
        self.installer.uninstallProducts(['ade25.base'])
        self.assertFalse(self.installer.isProductInstalled('ade25.base'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IAde25BaseLayer is registered."""
        from ade25.base.interfaces import IAde25BaseLayer
        from plone.browserlayer import utils
        self.failUnless(IAde25BaseLayer in utils.registered_layers())
