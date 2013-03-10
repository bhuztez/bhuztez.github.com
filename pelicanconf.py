#!/usr/bin/env python

import pelican
import pelican.writers
import pelican.generators
from pelican.utils import set_date_tzinfo

import os.path
from jinja2 import Markup


class Writer(pelican.writers.Writer):

    def _add_item_to_the_feed(self, feed, item):
        title = Markup(item.title).striptags()
        feed.add_item(
            title=title,
            link='%s/%s' % (self.site_url, item.url),
            # to be compatible with my ill-defined post-id when using jekyll
            unique_id='%s/%s/%s' % (self.site_url, item.date.strftime('%Y/%m'), item.slug),
            description=item.get_content(self.site_url),
            categories=item.tags if hasattr(item, 'tags') else None,
            author_name=getattr(item, 'author', ''),
            pubdate=set_date_tzinfo(item.date,
                self.settings.get('TIMEZONE', None)))


class StaticGenerator(pelican.generators.StaticGenerator):

    def _copy_paths(self, paths, source, destination, output_path,
            final_path=None):
        return super(StaticGenerator, self)._copy_paths(paths, source, 'css', output_path, final_path)


class Pelican(pelican.Pelican):

    def get_generator_classes(self):
        generators = super(Pelican, self).get_generator_classes()
        generators[0] = StaticGenerator
        return generators


    def get_writer(self):
        return Writer(self.output_path, settings=self.settings)


PUBLISH = False

PELICAN_CLASS = Pelican
THEME = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'theme')
THEME_STATIC_PATHS = ('css',)

AUTHOR = u'bhuztez'
SITENAME = u'H4 H4 0NLY S3RI0US'
SITEURL = 'http://bhuztez.github.com'
GITHUB_URL = 'https://github.com/bhuztez'
DISQUS_SITENAME = 'bhuztez-github-com'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'zh'

DEFAULT_PAGINATION = False

LOCALE = "C"

# MD_EXTENSIONS = ('codehilite(css_class=highlight)',) # 'footnotes'

ARTICLE_DIR = 'posts'
ARTICLE_EXCLUDES = ()
MARKUP = ('rst', 'markdown')
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}.html'
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'
DISPLAY_PAGES_ON_MENU = False
DEFAULT_DATE_FORMAT = '%Y-%m-%d'

# turn off unwanted pages
AUTHOR_SAVE_AS = False
CATEGORY_SAVE_AS = False
CATEGORIES_SAVE_AS = False
TAG_SAVE_AS = False
TAGS_SAVE_AS = False
ARCHIVES_SAVE_AS = 'posts/index.html'

CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = False
FEED_ALL_ATOM = 'feed.atom'

FILES_TO_COPY = (('robots.txt', 'robots.txt'),)



