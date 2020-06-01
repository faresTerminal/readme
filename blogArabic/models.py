from django.shortcuts import reverse, Http404
from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.postgres.fields import JSONField
import hashlib
from colorful.fields import RGBColorField
from django.utils import timezone 
from django.template.defaultfilters import slugify
from tinymce.models import HTMLField
from sorl.thumbnail import ImageField


# Create your models here.


def arabic_slugify(str):
    str = str.replace(" ", "-")
    str = str.replace(" ' ", "-")
    str = str.replace('"', '-')
    str = str.replace(" ّ ", "-")
    str = str.replace(".", "")
    str = str.replace("،", "-")
    str = str.replace(",", "-")
    str = str.replace("(", "-")
    str = str.replace(")", "")
    str = str.replace("؟", "")
    return str



class Category(models.Model):
    name = models.CharField(max_length=200)
    image_category = models.ImageField(null = True, blank = True, upload_to = 'Category_images')
    color = RGBColorField(colors=['#FF0000', '#00FF00', '#0000FF', '#17a589'])
    slug = models.SlugField(max_length=250, allow_unicode=True)
    
    
    

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
   
   

   

  



class author(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
   
    profile_picture = models.ImageField(blank = True, upload_to = 'Avatar', default= 'Avatar/deafult-profile-image.png')
    job = models.CharField(max_length = 500, blank = True, null = True)
    firstname = models.CharField(max_length = 500, blank = True, null = False)
   
    age = models.IntegerField(blank = True, null = True)
    gender = models.CharField(max_length = 500, blank = True, null = True)
    pays = models.CharField(max_length = 500, blank = True, null = True)
    level = models.CharField(max_length = 500, blank = True, null = True)
    facebook_account = models.CharField(max_length = 500, blank = True, null = True)
    instagram_account = models.CharField(max_length = 500, blank = True, null = True)
    youtube_channel = models.CharField(max_length = 500, blank = True, null = True)
    twitter_account = models.CharField(max_length = 500, blank = True, null = True)
   

    def read(self):
        # 总阅读量
        bs = articles.objects.only("read").filter(author_id=self.id)
        return sum([b.read for b in bs])

    read.short_description = "阅读量"


   

    def __str__(self):
        return self.name.username


    


class articles(models.Model):
    article_author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, max_length=200, on_delete=models.CASCADE)
    avatar = models.ForeignKey(author, on_delete = models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    featured = models.BooleanField(default=False)
    

    title = models.CharField('العنوان', max_length=9500)
    slug = models.SlugField(max_length=9500, unique_for_date='publish', allow_unicode=True)
    image = models.ImageField('صورة مناسبة', upload_to = 'Images')
    taker_image = models.CharField('ملتقط الصورة', max_length=200)
    source = models.CharField('المصدر', max_length=200)
    body = HTMLField()
    previous_post = models.ForeignKey(
        'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

   

    posted_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, auto_now_add=False)
    read = models.PositiveIntegerField(default=0, verbose_name='阅读数')
    publish = models.DateTimeField(default=timezone.now) 
   
    
    
    
    def __str__(self):
        return '%s %s %s' % (self.title, '/', self.category)

    def snippet(self):
        return '%s %s ' % (self.body[:120], '......' )

    def snippet1(self):
        return '%s %s ' % (self.body[:200], '......' )

    def snippet2(self):
        return '%s %s ' % (self.body[:100], '......' )

    def small_title(self):
        return '%s %s ' % (self.title[:40], '......' )

    
    def total_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
    
        if not self.slug:
            self.slug = slugify(self.title)
            if not self.slug:
                self.slug = arabic_slugify(self.title)

        super(articles, self).save(*args, **kwargs)

    



    


    def is_featured(self):
        return self.featured

    def is_read(self):
        return self.read

    def get_absolute_url(self):
        return reverse('blogArabic:show_article', kwargs={'id':self.id, 'slug': self.slug})
    @property
    def comment_count(self):
        return comment_put.objects.filter(user_put=self).count()

   

class Visit(models.Model):
    post = models.ForeignKey(articles, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
    visit_count = models.IntegerField(default=0)

   



class contactModel(models.Model):
    
    
    username1 = models.CharField(max_length = 500, blank = True, null = True)
    email = models.CharField(max_length = 500, blank = True, null = True)
    text_body = models.TextField(max_length = 500, blank = True, null = True)

    def __str__(self):
        return self.username1




class comment_put(models.Model):

    user_comment = models.ForeignKey(User, default = None, on_delete = models.CASCADE)
    user_put = models.ForeignKey(articles, on_delete = models.CASCADE)
    avatar_commenter = models.ForeignKey(author, on_delete = models.CASCADE)
    comment = models.TextField(max_length = 500)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
   
    def __str__(self):
        return self.comment


class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, related_name="following", on_delete = models.CASCADE)

    following_user_id = models.ForeignKey(author, related_name="followers", on_delete = models.CASCADE)

    # You can even add info about when user started following
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} follows {}'.format(self. user_id,
                                      self.following_user_id)
