# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse


class BlogTest(TestCase):
    """
    Tests of ``blog`` application.    
    """
    fixtures = ['test_data']
    
    def test_entry_archive_index(self):
        """
        Tests ``entry_archive_index`` view.
        """
        response = self.client.get(reverse('blog'))
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/entry_archive.html')

    def test_entry_archive_year(self):
        """
        Tests ``entry_archive_year`` view.
        """
        response = self.client.get(reverse('blog_year', args=['2010']))
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/entry_archive_year.html')
        
    def test_entry_archive_month(self):
        """
        Tests ``entry_archive_month``view.
        """
        response = self.client.get(reverse('blog_month', args=['2010', '07']))
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/entry_archive_month.html')
        
    def test_entry_archive_day(self):
        """
        Tests ``entry_archive_day`` view.
        """
        response = self.client.get(reverse('blog_day', args=['2010', '07', '21']))
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/entry_archive_day.html')
        
    def test_entry_detail(self):
        """
        Tests ``entry_detail`` view.
        """
        response = self.client.get(reverse('blog_entry', args=['2010', '07', '21', 'test-entry']))
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/entry_detail.html')
        
    def test_entry_detail_not_found(self):
        """
        Test ``entry_detail`` view with an offline entry.
        """
        response = self.client.get(reverse('blog_entry', args=['2010', '07', '21', 'offline-entry']))
        self.failUnlessEqual(response.status_code, 404)
        
    def test_category_detail(self):
        """
        Tests ``category_detail`` view.
        """
        response = self.client.get(reverse('blog_category', args=['test']))
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/category_detail.html')
        
    def test_category_detail_not_found(self):
        """
        Tests ``category_detail`` view with an offline category.
        """
        response = self.client.get(reverse('blog_category', args=['offline']))
        self.failUnlessEqual(response.status_code, 404)
        
    def test_rss_entries(self):
        """
        Tests entries RSS feed.
        """
        blog_url = reverse('blog')
        url = u'%sfeed/rss/entries/' % blog_url
        response = self.client.get(url)
        self.failUnlessEqual(response.status_code, 200)
        
    def test_rss_category(self):
        """
        Tests categories RSS feed.
        """
        from website.apps.blog.models import Category
        categories = Category.online_objects.all()
        blog_url = reverse('blog')
        for category in categories:
            url = u'%sfeed/rss/category/%s/' % (blog_url, category.slug)
            response = self.client.get(url)
            self.failUnlessEqual(response.status_code, 200)
