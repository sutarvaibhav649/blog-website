import re
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User
from . import models
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import PostForm
from django.contrib import messages
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


def category_view(request, slug):
    category = get_object_or_404(models.Category, slug=slug)
    posts = models.BlogPost.objects.filter(category=category, is_published=True).order_by('-created_at')
    return render(request, 'category_posts.html', {
        'category': category,
        'posts': posts
    })


def register_view(request):
    errors = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        profile_image = request.FILES.get('profile')

        # Username and email validations
        if not username:
            errors['username'] = "Username is required."
        elif User.objects.filter(username=username).exists():
            errors['username'] = "Username already taken."

        if not email:
            errors['email'] = "Email is required."
        elif User.objects.filter(email=email).exists():
            errors['email'] = "Email already registered."

        # Password validations
        if not password1:
            errors['password1'] = "Password is required."
        else:
            if len(password1) < 8:
                errors['password1'] = "Password must be at least 8 characters."
            elif not re.search(r'\d', password1):
                errors['password1'] = "Password must contain at least one digit."
            elif not re.search(r'[a-z]', password1):
                errors['password1'] = "Password must contain a lowercase letter."
            elif not re.search(r'[A-Z]', password1):
                errors['password1'] = "Password must contain an uppercase letter."
            elif not re.search(r'[~!@#$%^&*()_+=\[{\]};:<>|./?,-]', password1):
                errors['password1'] = "Password must contain a special character."

        if not password2:
            errors['password2'] = "Confirm password is required."
        elif password1 != password2:
            errors['password2'] = "Passwords do not match."

        # If everything is valid, register the user
        if not errors:
            user = User.objects.create_user(username=username, email=email, password=password1)
            # Handle profile image saving (see step 2)
            if profile_image:
                user.profile.profile_image = profile_image
                user.profile.save()

                login(request, user)
            return redirect('home_view')

    return render(request, 'users/register.html', {'errors': errors})


def login_view(request):
    errors = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')

        # Basic validations
        if not username:
            errors['username'] = "Username is required."
        if not password1:
            errors['password1'] = "Password is required."

        if not errors:
            user = authenticate(request, username=username, password=password1)
            if user is not None:
                login(request, user)

                request.session['username'] = user.username

                return redirect('home_view')
            else:
                errors['password1'] = "Invalid username or password."

    return render(request, 'users/login.html', {'errors': errors})


def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('home_view')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            models.BlogPost = form.save(commit=False)
            models.BlogPost.author = request.user
            models.BlogPost.save()
            return redirect('home_view')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def delete_post(request, slug):
    post = get_object_or_404(models.BlogPost, slug=slug)
    if post.author == request.user:
        post.delete()
        return redirect('home_view')
    return render(request, 'home_view')  

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home_view')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})
