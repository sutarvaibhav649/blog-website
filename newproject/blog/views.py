from django.shortcuts import render,get_object_or_404
from . import models
from django.views.generic import ListView
# Create your views here.
def home_view(request):
    posts = models.BlogPost.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

def blog_detail_view(request, slug):
    post = get_object_or_404(models.BlogPost, slug=slug, is_published=True)
    comments = models.Comment.objects.filter(blog=post, parent=None).order_by('-created_at')  # Top-level comments only
    return render(request, 'blog_detail.html', {'post': post, 'comments': comments})