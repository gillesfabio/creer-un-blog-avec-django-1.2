# -*- coding: utf-8 -*-
"""
Models of ``blog`` application.

"""
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from website.apps.blog.managers import CategoryOnlineManager
from website.apps.blog.managers import EntryOnlineManager


class Category(models.Model):
    """
    A blog category.    
    """
    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255, unique=True)
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)
    
    objects = models.Manager()
    online_objects = CategoryOnlineManager()
    
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        
    def __unicode__(self):
        return u'%s' % self.name

    @models.permalink
    def get_absolute_url(self):
        return ('blog_category', (), {
            'slug': self.slug,
        })

    def _get_online_entries(self):
        """
        Returns Entries in this Category with status of "online".
        Access this through the property ``online_entry_set``.        
        """
        from website.apps.blog.models import Entry
        return self.entry_set.filter(status=Entry.STATUS_ONLINE)
    online_entry_set = property(_get_online_entries)


class Entry(models.Model):
    """
    A blog entry.
    """
    STATUS_OFFLINE = 0
    STATUS_ONLINE = 1
    STATUS_DEFAULT = STATUS_OFFLINE
    STATUS_CHOICES = (
        (STATUS_OFFLINE, _('Offline')),
        (STATUS_ONLINE, _('Online')),
    )
    
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255, unique_for_date='publication_date')
    author = models.ForeignKey('auth.User', verbose_name=_('author'))
    category = models.ForeignKey(Category, verbose_name=_('category'))
    creation_date = models.DateTimeField(_('creation date'), auto_now_add=True)
    modification_date = models.DateTimeField(_('modification date'), auto_now=True)
    publication_date = models.DateTimeField(_('publication date'), default=datetime.now(), db_index=True)
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=STATUS_DEFAULT, db_index=True)
    body = models.TextField(_('body'))
    
    objects = models.Manager()
    online_objects = EntryOnlineManager()
    
    class Meta:
        verbose_name = _('entry')
        verbose_name_plural = _('entries')
    
    def __unicode__(self):
        return u'%s' % self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blog_entry', (), {
            'year': self.publication_date.strftime('%Y'),
            'month': self.publication_date.strftime('%m'),
            'day': self.publication_date.strftime('%d'),
            'slug': self.slug,
        })
