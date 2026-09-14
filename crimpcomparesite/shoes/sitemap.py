from django.contrib.sitemaps import Sitemap
from .models import Shoe, Guide, Category
from django.urls import reverse

class ShoeSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Shoe.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

class GuideSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Guide.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_at
    
class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Category.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_at
    

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['home', 'contact', 'deals', 'blog', 'guides', 'dictionary', 'categories', 'disclaimer','quiz_form']

    def location(self, item):
        return reverse(item)