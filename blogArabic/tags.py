
from django import template
from blogArabic.models import articles
from libs.display.models import Division
from django.db import models




@register.inclusion_tag('navigation.html')
def navigation(selected_id=None):
    return {
        'navigation': articles.objects.all(),
        'selected':selected_id,
    }