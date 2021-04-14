from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('create/post/', views.CreatePost.as_view(), name='create-post'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('category', views.CategoryList.as_view(), name='category-list'),
    path('category/<slug:slug>', views.CategoryDetail.as_view(), name='category-detail'),
    path('create/category/', views.CreateCategory.as_view(), name='create-category'),
]
