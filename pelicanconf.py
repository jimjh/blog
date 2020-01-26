#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'James Lim'
SITENAME = u'Ampersand'
SITEURL = 'https://blog.jimjh.com'
FEED_DOMAIN = 'http://feeds.feedburner.com'

PLUGIN_PATHS = ['../pelican-plugins']
PLUGINS = ['assets', 'sitemap']
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

TIMEZONE = 'US/Pacific'
THEME = 'pelican-svbhack'

DEFAULT_LANG = u'en'
TYPOGRIFY = False

# Feed generation is usually not desired when developing
FEED_ALL_ATOM    = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

LINKS = (
    ('Medium', 'https://medium.com/@jimjh'),
    ('Profile', 'https://jimjh.com')
)

DEFAULT_PAGINATION = 10
REVERSE_ARCHIVE_ORDER = True
DISPLAY_CATEGORIES_ON_MENU = False
HIDE_USER_LOGO = True
TAGLINE = "Moved to Medium in 2019."

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

FOOTER_TEXT   = """
<a href='https://jimjh.com'>James Lim</a> &sdot;
<a href='https://github.com/jimjh'>GitHub</a> &sdot;
<a href='https://www.linkedin.com/in/jimjh'>LinkedIn</a> &sdot;
<a href='https://stackoverflow.com/users/473709/james-lim'>StackOverflow</a>
"""

STATIC_PATHS = ['images', 'downloads', 'favicon.ico', 'CNAME']
WEBASSETS    = True

USER_LOGO_URL    = 'https://blog.jimjh.com/images/jimjh.png'
FB_ADMIN         = 'jimjh'
GCSE_ID          = '012036467613918901085:pygogpk_gsc'
