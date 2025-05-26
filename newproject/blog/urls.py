from django.urls import path
from . import views
urlpatterns = [
    path("",views.home_view,name="home_view"),
    path('blog/<slug:slug>/', views.blog_detail_view, name='blog-detail'),
]