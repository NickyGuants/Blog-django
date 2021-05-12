from django import template
from ..models import BlogPost

register = template.Library()
@register.inclusion_tag('blog/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = BlogPost.objects.filter(status=1).order_by('-created_at')[:count]
    return {'latest_posts': latest_posts}