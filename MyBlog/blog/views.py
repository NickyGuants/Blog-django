from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import BlogPost, Category


# Create your views here.
#Category
class CategoryList(ListView):
    model =Category
    template_name='blog/category_list.html'

class CategoryDetail(DetailView):
    model = Category
    template_name = 'blog/category_detail.html'


#Blog posts
class PostList(ListView):
    model = BlogPost
    queryset = BlogPost.objects.filter(status=1).order_by('-created_at')
    template_name = 'blog/index.html'

class PostDetail(DetailView):
    model = BlogPost
    template_name = 'blog/post_detail.html'