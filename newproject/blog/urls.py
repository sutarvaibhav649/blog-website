from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 
urlpatterns = [
    path("",views.home_view,name="home_view"),
    path('blog/<slug:slug>/', views.blog_detail_view, name='blog-detail'),
    path('comment/<int:pk>/edit/', views.edit_comment_view, name='edit-comment'),
    path('comment/<int:pk>/delete/', views.delete_comment_view, name='delete-comment'),
    path('category/<slug:slug>/', views.category_view, name='category-posts'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create-post/', views.create_post, name='create_post'),
    path('delete-post/<slug:slug>/', views.delete_post, name='delete_post'),

]