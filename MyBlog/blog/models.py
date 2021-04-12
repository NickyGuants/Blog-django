from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
STATUS = (
    (0, 'Draft'),
    (1, 'Published')
)


class Category(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='Categories')
    slug = models.SlugField(max_length=200, unique=True)


    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('category-detail', args=[str(self.id)])

    def __str__(self):
        return self.title


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
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        return self.title
