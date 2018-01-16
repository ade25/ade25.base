# -*- coding: utf-8 -*-
"""Module providing custom navigation strategy"""
from Products.CMFPlone.browser.navtree import DefaultNavtreeStrategy
from Products.Five import BrowserView
from plone import api
from plone.app.layout.navigation.navtree import buildFolderTree


class SiteNavigation(BrowserView):

    def __call__(self):
        return self.render()

    def render(self):
        return self.index()

    def build_nav_tree(self, root, query):
        """
        Create a list of portal_catalog queried items

        @param root: Content item which acts as a navigation root

        @param query: Dictionary of portal_catalog query parameters

        @return: Dictionary of navigation tree
        """

        # Navigation tree base portal_catalog query parameters
        applied_query = {
            'path': '/'.join(root.getPhysicalPath()),
            'sort_on': 'getObjPositionInParent'
        }
        # Apply caller's filters
        applied_query.update(query)
        # - use navigation portlet strategy as base
        strategy = DefaultNavtreeStrategy(root)
        strategy.rootPath = '/'.join(root.getPhysicalPath())
        strategy.showAllParents = False
        strategy.bottomLevel = 999
        # This will yield out tree of nested dicts of
        # item brains with retrofitted navigational data
        tree = buildFolderTree(root, root, query, strategy=strategy)
        return tree

    def nav_items(self):
        portal = api.portal.get()
        nav_tree_query = {
            'portal_type': [
                'ade25.sitecontent.sectionfolder',
                'ade25.sitecontent.contentpage'
            ]
        }
        brains = self.build_nav_tree(
            portal,
            query=nav_tree_query
        )
        return brains

