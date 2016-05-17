# Extend the FeedController class in order to fix
# the bug with atom feeds and multiple authors
# https://jira.landcareresearch.co.nz/browse/CKAN-128
#
# imports
import logging
import urlparse

import webhelpers.feedgenerator
from pylons import config

import ckan.model as model
import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.logic as logic

from ckan.common import _, g, c, request, response, json
from ckan.controllers.feed import FeedController
from ckan.controllers.feed import _FixedAtom1Feed
from ckan.controllers.feed import _package_search
from ckan.controllers.feed import _create_atom_id

class LCRNZFeedController(FeedController):

   # copied this method from FeedControler
    # only removed '/' from ids.
    def _group_or_organization(self, obj_dict, is_org):
        data_dict, params = self._parse_url_params()
        key = 'owner_org' if is_org else 'groups'
        data_dict['fq'] = '%s:"%s"' % (key, obj_dict['id'],)
        group_type = 'organization'
        if not is_org:
            group_type = 'group'

        item_count, results = _package_search(data_dict)

        navigation_urls = self._navigation_urls(params,
                                                item_count=item_count,
                                                limit=data_dict['rows'],
                                                controller='feed',
                                                action=group_type,
                                                id=obj_dict['name'])
        feed_url = self._feed_url(params,
                                  controller='feed',
                                  action=group_type,
                                  id=obj_dict['name'])

        guid = _create_atom_id(u'feeds/group/%s.atom' %
                               obj_dict['name'])
        alternate_url = self._alternate_url(params, groups=obj_dict['name'])
        desc = u'Recently created or updated datasets on %s by group: "%s"' %\
            (g.site_title, obj_dict['title'])
        title = u'%s - Group: "%s"' %\
            (g.site_title, obj_dict['title'])

        if is_org:
            guid = _create_atom_id(u'feeds/organization/%s.atom' %
                                   obj_dict['name'])
            alternate_url = self._alternate_url(params,
                                                organization=obj_dict['name'])
            desc = u'Recently created or  updated datasets on %s '\
                'by organization: "%s"' % (g.site_title, obj_dict['title'])
            title = u'%s - Organization: "%s"' %\
                (g.site_title, obj_dict['title'])

        return self.output_feed(results,
                                feed_title=title,
                                feed_description=desc,
                                feed_link=alternate_url,
                                feed_guid=guid,
                                feed_url=feed_url,
                                navigation_urls=navigation_urls)

    ## removed '/' from feeds
    def tag(self, id):
        data_dict, params = self._parse_url_params()
        data_dict['fq'] = 'tags:"%s"' % id

        item_count, results = _package_search(data_dict)

        navigation_urls = self._navigation_urls(params,
                                                item_count=item_count,
                                                limit=data_dict['rows'],
                                                controller='feed',
                                                action='tag',
                                                id=id)

        feed_url = self._feed_url(params,
                                  controller='feed',
                                  action='tag',
                                  id=id)

        alternate_url = self._alternate_url(params, tags=id)

        return self.output_feed(results,
                                feed_title=u'%s - Tag: "%s"' %
                                (g.site_title, id),
                                feed_description=u'Recently created or '
                                'updated datasets on %s by tag: "%s"' %
                                (g.site_title, id),
                                feed_link=alternate_url,
                                feed_guid=_create_atom_id
                                (u'feeds/tag/%s.atom' % id),
                                feed_url=feed_url,
                                navigation_urls=navigation_urls)


    ## removed '/' from feeds
    def general(self):
        data_dict, params = self._parse_url_params()
        data_dict['q'] = '*:*'

        item_count, results = _package_search(data_dict)

        navigation_urls = self._navigation_urls(params,
                                                item_count=item_count,
                                                limit=data_dict['rows'],
                                                controller='feed',
                                                action='general')

        feed_url = self._feed_url(params,
                                  controller='feed',
                                  action='general')

        alternate_url = self._alternate_url(params)

        return self.output_feed(results,
                                feed_title=g.site_title,
                                feed_description=u'Recently created or '
                                'updated datasets on %s' % g.site_title,
                                feed_link=alternate_url,
                                feed_guid=_create_atom_id
                                (u'feeds/dataset.atom'),
                                feed_url=feed_url,
                                navigation_urls=navigation_urls)


    # copied this method from FeedControler
    # only changed how author's are processed.
    def output_feed(self, results, feed_title, feed_description,
                    feed_link, feed_url, navigation_urls, feed_guid):
        author_name = config.get('ckan.feeds.author_name', '').strip() or \
            config.get('ckan.site_id', '').strip()
        author_link = config.get('ckan.feeds.author_link', '').strip() or \
            config.get('ckan.site_url', '').strip()

        # TODO language
        feed = _FixedAtom1Feed(
            title=feed_title,
            link=feed_link,
            description=feed_description,
            language=u'en',
            author_name=author_name,
            author_link=author_link,
            feed_guid=feed_guid,
            feed_url=feed_url,
            previous_page=navigation_urls['previous'],
            next_page=navigation_urls['next'],
            first_page=navigation_urls['first'],
            last_page=navigation_urls['last'],
        )

        for pkg in results:
            feed.add_item(
                title=pkg.get('title', ''),
                link=self.base_url + h.url_for(controller='package',
                                               action='read',
                                               id=pkg['id']),
                description=pkg.get('notes', ''),
                updated=h.date_str_to_datetime(pkg.get('metadata_modified')),
                published=h.date_str_to_datetime(pkg.get('metadata_created')),
                unique_id=_create_atom_id(u'dataset/%s' % pkg['id']),
                author_name=';'.join(str(x) for x in pkg.get('author','')),
                author_email=pkg.get('author_email', ''),
                categories=[t['name'] for t in pkg.get('tags', [])],
                enclosure=webhelpers.feedgenerator.Enclosure(
                    self.base_url + h.url_for(controller='api',
                                              register='package',
                                              action='show',
                                              id=pkg['name'],
                                              ver='2'),
                    unicode(len(json.dumps(pkg))),   # TODO fix this
                    u'application/json')
            )
        response.content_type = feed.mime_type
        return feed.writeString('utf-8')
