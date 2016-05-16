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
