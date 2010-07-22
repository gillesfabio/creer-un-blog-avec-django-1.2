# -*- coding: utf-8
"""
Feeds of ``blog`` application.
"""
from django.utils.feedgenerator import Rss201rev2Feed
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse

from django.contrib.syndication import feeds
from django.contrib.sites.models import Site

from website.apps.blog.models import Entry
from website.apps.blog.models import Category


class RssEntries(feeds.Feed):
    """
    RSS entries.    
    """
    feed_type = Rss201rev2Feed
    title_template = "blog/feeds/entry_title.html"
    description_template = "blog/feeds/entry_description.html"
    
    def title(self):
        """ 
        Channel title. 
        """
        site = Site.objects.get_current()
        return _('%(site_name)s: RSS entries') % {
            'site_name': site.name,
        }
    
    def description(self):
        """
        Channel description.
        """
        site = Site.objects.get_current()
        return _('RSS feed of recent entries posted on %(site_name)s.') % {
            'site_name': site.name,
        }
        
    def link(self):
        """
        Channel link.
        """
        return reverse('blog')
    
    def items(self):
        """
        Channel items.
        """
        return Entry.online_objects.order_by('-publication_date')[:10]
    
    def item_pubdate(self, item):
        """
        Channel item publication date.
        """
        return item.publication_date


class RssCategory(RssEntries):
    """
    RSS category.    
    """
    
    def title(self, obj):
        """
        Channel title.    
        """
        site = Site.objects.get_current()
        return _('%(site_name)s: RSS %(category)s category') % {
            'site_name': site.name,
            'category': obj.name,
        }
    
    def description(self, obj):
        """
        Channel description.
        """
        site = Site.objects.get_current()
        return _('RSS feed of recent entries posted in the category %(category)s on %(site_name)s.') % {
            'category': obj.name,
            'site_name': site.name,
        }
        
    def link(self, obj):
        """
        Channel link.
        """
        return reverse('blog_category', args=[obj.slug])

    def get_object(self, bits):
        """
        Object: the Category.
        """
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Category.online_objects.get(slug=bits[0])
    
    def items(self, obj):
        """
        Channel items.
        """
        return obj.online_entry_set
    
    def item_pubdate(self, item):
        """
        Channel item publication date.
        """
        return item.publication_date
