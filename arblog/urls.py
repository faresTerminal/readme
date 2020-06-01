"""arblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
# to call static files module
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from blogArabic import views
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from blogArabic.sitemaps import PostSitemap

#### to active static when DEBUG = False ###
from django.views.static import serve
####################################"""" 

sitemaps = {
    'post': PostSitemap,
}
# this to 404.html work
handler404 = 'blogArabic.views.error_404_view'

urlpatterns = [
    
    # this to protect admin page(it is fuc admin page)
    url(r'^admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    # this the real admin login page
    path('pythonDZ/', admin.site.urls),
    
    url(r'^', include('blogArabic.urls', namespace= 'blog')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^robots\.txt$', TemplateView.as_view(template_name="blogArabic/robots.txt", content_type='text/plain')),

   
   
  
   

     # this to reset password via email
    path('', include('django.contrib.auth.urls')),

    path('sitemaps.xml',sitemap, {'sitemaps': sitemaps} ),
    #### to active static when DEBUG = False ###
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    ##########################################################################
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
