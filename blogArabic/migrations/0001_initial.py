# Generated by Django 2.0.9 on 2020-05-31 16:30

import colorful.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('featured', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=9500, verbose_name='العنوان')),
                ('slug', models.SlugField(allow_unicode=True, max_length=9500, unique_for_date='publish')),
                ('image', models.ImageField(upload_to='Images', verbose_name='صورة مناسبة')),
                ('taker_image', models.CharField(max_length=200, verbose_name='ملتقط الصورة')),
                ('source', models.CharField(max_length=200, verbose_name='المصدر')),
                ('body', tinymce.models.HTMLField()),
                ('posted_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('read', models.PositiveIntegerField(default=0, verbose_name='阅读数')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('article_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, default='Avatar/deafult-profile-image.png', upload_to='Avatar')),
                ('job', models.CharField(blank=True, max_length=500, null=True)),
                ('firstname', models.CharField(blank=True, max_length=500)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=500, null=True)),
                ('pays', models.CharField(blank=True, max_length=500, null=True)),
                ('level', models.CharField(blank=True, max_length=500, null=True)),
                ('facebook_account', models.CharField(blank=True, max_length=500, null=True)),
                ('instagram_account', models.CharField(blank=True, max_length=500, null=True)),
                ('youtube_channel', models.CharField(blank=True, max_length=500, null=True)),
                ('twitter_account', models.CharField(blank=True, max_length=500, null=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image_category', models.ImageField(blank=True, null=True, upload_to='Category_images')),
                ('color', colorful.fields.RGBColorField(colors=['#FF0000', '#00FF00', '#0000FF', '#17a589'])),
                ('slug', models.SlugField(allow_unicode=True, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='comment_put',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=500)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('avatar_commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogArabic.author')),
                ('user_comment', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_put', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogArabic.articles')),
            ],
        ),
        migrations.CreateModel(
            name='contactModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username1', models.CharField(blank=True, max_length=500, null=True)),
                ('email', models.CharField(blank=True, max_length=500, null=True)),
                ('text_body', models.TextField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('visit_count', models.IntegerField(default=0)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogArabic.articles')),
            ],
        ),
        migrations.AddField(
            model_name='articles',
            name='avatar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogArabic.author'),
        ),
        migrations.AddField(
            model_name='articles',
            name='category',
            field=models.ForeignKey(max_length=200, on_delete=django.db.models.deletion.CASCADE, to='blogArabic.Category'),
        ),
        migrations.AddField(
            model_name='articles',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='articles',
            name='next_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next', to='blogArabic.articles'),
        ),
        migrations.AddField(
            model_name='articles',
            name='previous_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous', to='blogArabic.articles'),
        ),
    ]
