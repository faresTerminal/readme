# Generated by Django 2.0.9 on 2020-05-31 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogArabic', '0002_author_follow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='follow',
        ),
    ]