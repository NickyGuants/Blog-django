from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('tag/<slug:tag_slug>/',views.post_list, name='post_list_by_tag'),
    path('user/<str:username>', views.UserPostList.as_view(), name='user-posts'),
    path('category/', views.CategoryList.as_view(), name='category-list'),
    path('new/post/', views.CreatePost.as_view(), name='create-post'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('<slug:slug>/update/', views.UpdatePost.as_view(), name='post-update'),
    path('<slug:slug>/delete/', views.PostDelete.as_view(), name='post-delete'),
    path('category/<slug:slug>', views.CategoryDetail.as_view(), name='category-detail'),
    path('new/category/', views.CreateCategory.as_view(), name='create-category'),
    path('<slug:slug>/share/',views.post_share, name='post-share'),
]
