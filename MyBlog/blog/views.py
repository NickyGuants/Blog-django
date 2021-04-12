from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import BlogPost


# Create your views here.
class PostList(ListView):
    model = BlogPost
    queryset = BlogPost.objects.filter(status=1).order_by('-created_at')
    template_name = 'blog/index.html'

class PostDetail(DetailView):
    model = BlogPost
    template_name = 'blog/post_detail.html'