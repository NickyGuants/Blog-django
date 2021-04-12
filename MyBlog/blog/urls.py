from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('category', views.CategoryList.as_view(), name='category-list'),
    path('category/<int:pk>', views.CategoryDetail.as_view(), name='category-detail'),
]
