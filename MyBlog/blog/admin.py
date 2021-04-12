from django.contrib import admin
from .models import Category, BlogPost, Comment


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'category')
    list_filter = ('category', 'status')
    search_fields = ['title', 'post']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category)
admin.site.register(BlogPost, PostAdmin)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

