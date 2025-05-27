from django.shortcuts import render,get_object_or_404,redirect
from . import models
from django.views.generic import ListView
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
# Create your views here.
def home_view(request):
    posts = models.BlogPost.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

def blog_detail_view(request, slug):
    post = get_object_or_404(models.BlogPost, slug=slug, is_published=True)
    comments = models.Comment.objects.filter(blog=post, parent=None).order_by('-created_at')
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = post
            comment.user = request.user  # Ensure user is logged in
            comment.save()
            return redirect('blog-detail', slug=slug)

    return render(request, 'blog_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })
    
@login_required    
def edit_comment_view(request ,pk):
    comment = get_object_or_404(models.Comment,pk=pk)
    
    if comment.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit comment")
    
    if request.method == 'POST':
        form = CommentForm(request.POST,instance = comment)
        if form.is_valid():
            form.save()
            return redirect('blog-detail', slug=comment.blog.slug)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'edit_comment.html', {'form': form})

@login_required
def delete_comment_view(request, pk):
    comment = get_object_or_404(models.Comment, pk=pk)

    if comment.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this comment.")

    if request.method == 'POST':
        blog_slug = comment.blog.slug
        comment.delete()
        return redirect('blog-detail', slug=blog_slug)

    return render(request, 'delete_comment.html', {'comment': comment})