from django.contrib.sitemaps import Sitemap
from blogArabic.models import articles


class PostSitemap(Sitemap):

	def items(self):
		return articles.objects.all()

