from django.contrib import admin

# Register your models here.
from django.contrib import admin

from blog import models

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title','create_timestamp')

admin.site.register(models.BlogPost,BlogPostAdmin)