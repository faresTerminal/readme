from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm

from .import views

app_name="blogArabic"
urlpatterns = [
    # home page
    url(r'^$', views.index, name='index'),
    #open login page
    url(r'^login/$', views.login, name = 'login'),
    #open register page
    url(r'^register/$', views.register, name = 'register'),

    #check login
    url(r'^auth/$', views.auth_views, name='auth_views'),

   # logout or Disconnect
   url(r'^logout/$', views.logout, name ='logout'),

   # create post
   url(r'create/$', views.create_article, name='create_article'),

   #publish
   url(r'publish/$', views.publish, name='publish'),

   #chose avatar
   url(r'avatar/$', views.avatar, name='avatar'),

   url(r'profile/$', views.getProfile, name="getProfile"),

   url(r'^like/$', views.like_post, name="like_post"),
  

  
   # about page
   url(r'about/$', views.about, name="about"),

   # contact page
   url(r'contact/$', views.contact, name="contact"),

   #show category
   url(r'show_category/$', views.show_category, name="show_category"),
   # to go to spicial id when click a link 
   url(r'article/(?P<id>\d+)/(?P<slug>[\w-]+)/$', views.show_article, name='show_article'),

   # TO SHOW PROFILE
   url(r'user/(?P<id>\d+)/$', views.show_profile, name='show_profile'),
   
   
   # show solo category articles
   url(r'topic/(?P<id>\d+)/(?P<slug>[\w-]+)/$', views.getTopic, name="getTopic"),
   #reset password page from email
   url(r'reset_password/$', views.reset_pass, name='reset_pass'),
   #send lik to reset password
   url(r'^password_email/$', views.send_pass_link, name='send_pass_link'),
   #faq page
   url(r'^faq/$', views.faq, name='faq'),
   #search page
   url(r'^search/$', views.search, name='search'),

   #contact add comment
   url(r'^contact_send/$', views.contact_comment, name='contact_comment'),
   
   url(r'delete/(?P<pid>\d+)/$', views.getDelete, name="getDelete"),
   url(r'update/(?P<pid>\d+)/$', views.getUpdate, name="getUpdate"),

   #change password from profile
   url(r'password_change/$', views.change_password, name='change_password'),

   #terms service
   url(r'terms_services/$', views.terms_service, name='terms_service'),

   #privacy page
   url(r'privacy/$', views.privacy, name='privacy'),
    #put comment to publish
   
   url(r'add_comment/(?P<id>\d+)/$', views.save_comment, name='save_comment'),
  



    # urls to change password user via Email ############################################################""
   url(r'^password_reset/$', auth_views.password_reset, {"template_name": "regi/password_reset_form.html", 
        "post_reset_redirect": "password_reset_done", "email_template_name": "regi/password_reset_email.html"}, name='password_reset'),

   url(r'^password_reset/done/$', auth_views.password_reset_done, {"template_name": "regi/password_reset_done.html"}, name='password_reset_done'),
        
   url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {"template_name": "regi/password_reset_confirm.html"}, name='password_reset_confirm'),
   url(r'^reset/done/$', auth_views.password_reset_complete, {"template_name": "regi/password_reset_complete.html"}, name='password_reset_complete'),
    ##############################################################################################
  
     #account confirmations
   path('activate/<uid>/<token>', views.activate, name="activate"),


   
    
    
]