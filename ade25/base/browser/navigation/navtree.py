# -*- coding: utf-8 -*-
"""Module providing catalog query based nav trees"""
from Products.CMFPlone import utils
from plone import api
from plone.app.layout.navigation.root import getNavigationRoot
from plone.i18n.normalizer import IIDNormalizer
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from plone.memoize.view import memoize_contextless
from zope.contentprovider.provider import ContentProviderBase

from ade25.base import config as ade25_config
from ade25.base.browser.controlpanel.settings import IAde25BaseControlPanelNavigation


class NavTreeProvider(ContentProviderBase):

    _nav_tree = None
    _nav_tree_path = None
    _nav_tree_context = None

    _opener_markup_template = (
        u'<span class="c-nav__link-item c-nav__link-item--icon">'  # noqa: E 501
        u'{opener}'
        u'</span>'
    )

    _item_markup_template = (
        u'<li class="c-nav__item c-nav__item-{id}{has_sub_class}{is_current}">'
        u'<a href="{url}" class="c-nav__link c-nav__link--default c-nav__link--state-{review_state}{dropdown_toggle}{js_class}"{aria_haspopup}><span class="c-nav__link-text">{title}</span>{opener}</a>'  # noqa: E 501
        u'{sub}'
        u'</li>'
    )

    _subtree_markup_wrapper = (
        u'<ul class="c-nav c-nav--level-{0} c-nav__dropdown c-nav__dropdown--hidden has_subtree dropdown" aria-label="submenu">{out}</ul>'  # noqa: E 501
    )

    @property
    @memoize_contextless
    def settings(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(
            IAde25BaseControlPanelNavigation,
            prefix='ade25.base')
        return settings

    @property
    def nav_tree_path(self):
        if self._nav_tree_path is None:
            self._nav_tree_path = getNavigationRoot(self.context)
        return self._nav_tree_path

    @property
    def nav_tree_depth(self):
        try:
            navigation_depth = self.settings.navigation_depth
        except (AttributeError, KeyError):
            navigation_depth = 3
        return navigation_depth

    @property
    def nav_tree_element_open(self):
        try:
            navigation_element = self.settings.navigation_element_open
        except (AttributeError, KeyError):
            navigation_element = ade25_config.navigation_elements(action='open')
        return navigation_element

    @property
    def enableDesc(self):
        return True

    @property
    def nav_tree(self):

        if self._nav_tree is not None:
            return self._nav_tree

        types = api.portal.get_registry_record(
            name='ade25.base.listed_content_types'
        )
        lang_current = api.portal.get_current_language()

        query = {
            'path': {'query': self.nav_tree_path, 'depth': self.nav_tree_depth},
            'portal_type': {'query': types},
            'exclude_from_toc': False,
            'review_state': 'published',
            'Language': lang_current,
            'sort_on': 'getObjPositionInParent'
        }
        brains = api.content.find(**query)

        ret = {}

        # Get current object path for later determine if it's current
        context_physical_path = self.context.getPhysicalPath()
        if utils.isDefaultPage(self.context, self.request):
            context_physical_path = context_physical_path[:-1]
        context_path = '/'.join(context_physical_path)

        for it in brains:
            brain_path = '/'.join(it.getPath().split('/'))
            is_current = False
            if context_path is not None:
                # Determine if it's current object
                is_current = context_path == it.getPath()
            path_key = '/'.join(it.getPath().split('/')[:-1])
            entry = {
                'id': it.id,
                'uid': it.UID,
                'path': brain_path,
                'url': it.getURL(),
                'title': utils.safe_unicode(it.Title),
                'review_state': it.review_state,
                'is_current': is_current
            }
            if path_key in ret:
                ret[path_key].append(entry)
            else:
                ret[path_key] = [entry]

        self._nav_tree = ret
        return ret

    def render_item(self, item, iteration):
        sub = self.build_tree(
            item['path'],
            first_run=False,
            iteration=iteration+1
        )
        if sub:
            item.update({
                'sub': sub,
                'opener':  self._opener_markup_template.format(
                    opener=self.nav_tree_element_open),
                'aria_haspopup': ' aria-haspopup="true"',
                'dropdown_toggle': ' js-dropdown-toggle',
                'has_sub_class': ' c-nav__item--has-children',
                'is_current': ' c-nav__item--current',
                'js_class': ' js-dropdown-toggle'
            })
        else:
            item.update({
                'sub': sub,
                'opener':  '',
                'aria_haspopup': '',
                'dropdown_toggle': '',
                'has_sub_class': '',
                'is_current': '',
                'js_class': ''
            })
        return self._item_markup_template.format(**item)

    def build_tree(self, path, first_run=True, iteration=0):
        """Non-template based recursive tree building.
        3-4 times faster than template based.
        """
        out = u''
        for item in self.nav_tree.get(path, []):
            out += self.render_item(item, iteration)

        if not first_run and out:
            out = self._subtree_markup_wrapper.format(iteration, out=out)
        return out

    def build_tree_deprecated(self, path, first_run=True, iteration=0):
        """Non-template based recursive tree building.
        3-4 times faster than template based.
        See figures below.
        """
        normalizer = getUtility(IIDNormalizer)
        out = u''
        for it in self.nav_tree.get(path, []):
            sub = self.build_tree(path + '/' + it['id'],
                                  first_run=False,
                                  iteration=iteration+1)
            opener = u"""<span class="c-nav__link--action">
                      <span class="c-nav__toggle c-nav__toggle--open">
                      {el}</span></span>""".format(
                uid=it['uid'],
                el=self.nav_tree_element_open,
                id=it['id']
            ) if sub else ''
            out += u"""<li class="c-nav__item 
                    c-nav__item--{id}{has_sub_class}{is_current}">""".format(
                id=normalizer.normalize(it['id']),
                has_sub_class=' c-nav__item--has-children' if sub else '',
                is_current=' c-nav__item--current' if it['is_current'] else ''
            )
            out += u"""<a href="{url}" class="c-nav__link c-nav__link--default 
                    c-nav__link--state-{review_state}{dropdown_toggle}"
                    aria-haspopup="true"><span class="c-nav__link-text">{title}
                    </span>{opener}</a>""".format(
                url=it['url'],
                review_state=it['review_state'],
                title=utils.safe_unicode(it['title']),
                dropdown_toggle=' js-dropdown-toggle' if sub else '',
                opener=opener if sub else ''
            )
            out += sub
            out += u'</li>'

        if not first_run:
            base_list = u"""<ul class="c-nav c-nav--level-{0} c-nav__dropdown 
                        c-nav__dropdown--hidden has_subtree dropdown" 
                        aria-label="submenu">""".format(
                iteration
            )
            out = base_list + out + u'</ul>' if out else ''
        return out

    def render(self):
        return self.build_tree(self.nav_tree_path)
