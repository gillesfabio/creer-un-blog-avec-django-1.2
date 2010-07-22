# -*- coding: utf-8 -*-
"""
URLs of ``blog`` application.
"""
from django.conf.urls.defaults import *

from website.apps.blog.models import Entry
from website.apps.blog.models import Category

from website.apps.blog.feeds import RssEntries
from website.apps.blog.feeds import RssCategory


rss_feeds = {
    'entries': RssEntries,
    'category': RssCategory,
}

urlpatterns = patterns('',
    url(r'^feed/rss/(?P<url>.*)/$', 
        'django.contrib.syndication.views.feed', 
        {'feed_dict': rss_feeds},
        name='blog_rss_feed',
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\w-]+)/$',
        'django.views.generic.date_based.object_detail',
        dict(
            queryset=Entry.online_objects.all(),
            month_format='%m',
            date_field='publication_date',
            slug_field='slug',
        ),
        name='blog_entry',
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        'django.views.generic.date_based.archive_day',
        dict(
            queryset=Entry.online_objects.all(),
            month_format='%m',
            date_field='publication_date',     
        ),
        name='blog_day',
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        'django.views.generic.date_based.archive_month',
        dict(
            queryset=Entry.online_objects.all(),
            month_format='%m',
            date_field='publication_date',
        ),
        name='blog_month',
    ),
    url(r'^(?P<year>\d{4})/$',
        'django.views.generic.date_based.archive_year',
        dict(
            queryset=Entry.online_objects.all(),
            make_object_list=True,
            date_field='publication_date',
        ),
        name='blog_year',
    ),
    url(r'^category/(?P<slug>[\w-]+)/$',
        'django.views.generic.list_detail.object_detail',
        dict(
            queryset=Category.online_objects.all(),
            slug_field='slug'
        ),
        name='blog_category',
    ),
    url(r'^$',
        'django.views.generic.date_based.archive_index', 
        dict(
            queryset=Entry.online_objects.all(),
            date_field='publication_date',
        ),
        name='blog',
    ),
)
