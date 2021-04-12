from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import BlogPost, Category
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404

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

def post_detail(request, slug):
    template_name ='post_detail.html'
    post=get_object_or_404(BlogPost, slug=slug)
    comments= post.comments.filter(active=True)
    new_comment=None

    #comment posted
    if request.method== 'POST':
        comment_form= CommentForm(data=request.POST)
        if comment_form.is_valid():
            #create comment object
            new_comment=comment_form.save(commit=False)
            #assign the current post to the comment
            new_comment.post= post
            # Now save the comment to the database
            new_comment.save()
    else:
        comment_form=CommentForm()

    return render(request, template_name, {'post': post, 
                                            'comments': comments, 
                                            'new_comment': new_comment, 
                                            'comment_form': comment_form})