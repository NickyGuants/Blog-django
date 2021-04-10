from django.contrib import admin
from .models import Category, BlogPost


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'category')
    list_filter = ('category', 'status')
    search_fields = ['title', 'post']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category)
admin.site.register(BlogPost, PostAdmin)
