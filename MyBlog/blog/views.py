from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import BlogPost, Category
from .forms import CommentForm,EmailPostForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from taggit.models import Tag

# Create your views here.
#Category
class CategoryList(ListView):
    model =Category
    template_name='blog/category_list.html'
    paginate_by= 5

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
    paginate_by= 5
    
def post_list(request,tag_slug=None):
    queryset = BlogPost.objects.filter(status=1).order_by('-created_at')
    #post_list=BlogPost.objects.all()
    paginator=Paginator(queryset, 3)
    template_name = 'blog/index.html'
    tag=None

    if tag_slug:
        tag=get_object_or_404(Tag, slug=tag_slug)
        queryset=queryset.filter(tags__in=[tag])
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, template_name, {'posts': posts,'tag': tag})

class UserPostList(ListView):
    model = BlogPost
    template_name = 'blog/user_posts.html'
    paginate_by= 5
    
    def get_queryset(self):
        user= get_object_or_404(User, username= self.kwargs.get('username'))
        return BlogPost.objects.filter(author=user).order_by('-created_at')
        

class CreatePost(LoginRequiredMixin,CreateView):
    model= BlogPost
    fields = ['title','post', 'status', 'category']
    template_name= 'blog/post_form.html'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class UpdatePost(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model= BlogPost
    fields = ['title','post', 'status', 'category','tags']
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
                                            'comment_form': comment_form
                                            }
                                            )

def post_share(request,slug):
# Retrieve post by id
    post = get_object_or_404(BlogPost,id=slug)
    sent=False

    if request.method == 'POST':
    # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
            post_url = request.build_absolute_uri(
            post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
            f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
            f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'tembeguants@gmail.com',
            [cd['receipient']])
            sent = True
            return render(request, 'blog/post_detail.html', {'post': post,'form': form})
    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', {'post': post,'form': form})