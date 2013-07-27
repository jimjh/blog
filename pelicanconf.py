#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Jim Lim'
SITENAME = u'Ampersand'
SITEURL = 'http://blog.jimjh.com'
FEED_DOMAIN = 'http://feeds.feedburner.com'
SITE_DOMAIN = 'http://blog.jimjh.com' # for generating external URLs

PLUGIN_PATH = '../pelican-plugins'
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
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

LINKS = (
    ('Profile', 'http://jimjh.com'),
)

DEFAULT_PAGINATION = 10
REVERSE_ARCHIVE_ORDER = True

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

FOOTER_TEXT   = """
<a href='http://jimjh.com'>Jim Lim</a> &sdot;
<a href='https://plus.google.com/111805949132881507016' rel='author'>G+</a>
&sdot;
<a href='https://github.com/jimjh'>GitHub</a> &sdot;
<a href='http://www.linkedin.com/in/jimjh'>LinkedIn</a> &sdot;
<a href='http://stackoverflow.com/users/473709/jim-lim'>StackOverflow</a>
"""

STATIC_PATHS = ['images', 'downloads']
WEBASSETS    = True
FILES_TO_COPY = (
    ('extra/favicon.ico', 'favicon.ico'),
    ('extra/CNAME', 'CNAME'),
)

FEED_ALL_RSS     = 'jimjh/blog'
FEED_ALL_ATOM    = 'jimjh/blog'

DISQUS_SITENAME  = 'jimjh'
GOOGLE_ANALYTICS = 'UA-5604647-6'
USER_LOGO_URL    = 'http://blog.jimjh.com/static/images/jimjh.png'
FB_ADMIN         = 'jimjh'
MAILCHIMP_URL    = 'http://jimjh.us7.list-manage.com/subscribe/post?u=384f06163c70729da8e51b396&amp;id=162cf33799'
GCSE_ID          = '012036467613918901085:pygogpk_gsc'
