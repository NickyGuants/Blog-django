from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import BlogPost, Category
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
#Category
class CategoryList(ListView):
    model =Category
    template_name='blog/category_list.html'

class CategoryDetail(DetailView):
    model = Category
    template_name = 'blog/category_detail.html'

class CreateCategory(LoginRequiredMixin,CreateView):
    model= Category
    fields=['title']
    template_name= 'blog/category_form.html'

#Blog posts
class PostList(ListView):
    model = BlogPost
    queryset = BlogPost.objects.filter(status=1).order_by('-created_at')
    template_name = 'blog/index.html'

class CreatePost(LoginRequiredMixin,CreateView):
    model= BlogPost
    fields = ['title','post', 'status', 'category']
    template_name= 'blog/post_form.html'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class UpdatePost(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model= BlogPost
    fields = ['title','post', 'status', 'category']
    template_name= 'blog/post_update.html'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False
class PostDelete(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = BlogPost
    template_name = 'blog/post_confirm_delete.html'
    success_url='/'
    def test_func(self):
        post=self.get_object()
        if self.request.user == post.author:
            return True
        return False

@login_required
def post_detail(request, slug):
    template_name ='blog/post_detail.html'
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