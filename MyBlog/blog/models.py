from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify # new

# Create your models here.
STATUS = (
    (0, 'Draft'),
    (1, 'Published')
)


class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)


    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('category-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class BlogPost(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    post = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('post_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs): # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class Comment(models.Model):
    post=models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name=models.CharField(max_length=100)
    email=models.EmailField()
    body=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=False)

    class Meta:
        ordering= ['created_on']

    def __str__(self):
        return 'Cooment {} by {}'. format(self.body,self.name)
