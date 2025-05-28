from django.urls import path
from . import views
urlpatterns = [
    path("",views.home_view,name="home_view"),
    path('blog/<slug:slug>/', views.blog_detail_view, name='blog-detail'),
    path('comment/<int:pk>/edit/', views.edit_comment_view, name='edit-comment'),
    path('comment/<int:pk>/delete/', views.delete_comment_view, name='delete-comment'),
    path('category/<slug:slug>/', views.category_view, name='category-posts'),

]