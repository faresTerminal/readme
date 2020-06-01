from django.contrib import admin

from django.contrib.auth.models import User

from .models import articles, author, Category, contactModel, comment_put, Visit

@admin.register(articles)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Category)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
 


 




# Register your mo


admin.site.register(comment_put)
admin.site.register(author)

admin.site.register(Visit)
admin.site.register(contactModel)


