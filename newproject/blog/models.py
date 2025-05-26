from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile/',null=True,blank=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.username
    

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(unique=True)
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

class Tag(models.Model):
    name = models.CharField(max_length=50,blank=True,unique=True)
    
    def __str__(self):
        return self.name
    

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True,blank=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey('Category',on_delete=models.SET_NULL,blank=True,null=True)
    tag = models.ManyToManyField('Tag',blank=True)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to='thumbnail/',blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def like_count(self):
        return self.likes.count()
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    blog = models.ForeignKey('BlogPost',on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True,related_name='replies')
    
    def __str__(self):
        return f'Comment by {self.user.username} on {self.blog.title[:30]}'
    

class Likes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    blog = models.ForeignKey('BlogPost',on_delete=models.CASCADE,related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'blog')
        
    def __str__(self):
        return f"{self.user.username} liked {self.blog.title[:30]}"