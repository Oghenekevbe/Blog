from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse
from ckeditor.fields import RichTextField

# Create your models here.



class Profile(models.Model):
    user = models.OneToOneField(User, null = True, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255, null = True,  blank = True)
    profile_pic = models.ImageField(null= True, blank = True)
    website_url = models.CharField(max_length=255, null = True,  blank = True)
    twitter_url = models.CharField(max_length=255, null = True,  blank = True)
    instagram_url = models.CharField(max_length=255, null = True,  blank = True)
    linkedin_url = models.CharField(max_length=255, null = True,  blank = True)


    def __str__(self):
        return str(self.user)

class Category(models.Model):
    name = models.CharField( max_length=200)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('index')






STATUS =(
    (0, 'draft'),
    (1, 'publish')
)
class Post(models.Model):
    title = models.CharField(max_length=100)
    title_tag = models.CharField(max_length=60)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default = datetime.now, blank= True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name = 'post_category', default = 'uncategorized')
    image = models.ImageField(null= True, blank = True)
    body = RichTextField()
    status = models.IntegerField(choices=STATUS,default=0)
    order = models.IntegerField(default=0)
    slug = models.SlugField()
    likes = models.ManyToManyField(User, related_name = 'blog_post')
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title + ' | ' + str(self.author)
    def get_absolute_url(self):
        return reverse('index')
    def total_likes(self):
        return self.likes.count()
   


    

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name = 'comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField( auto_now_add=True)
    
    def __str__(self):
        return self.author + ' | ' + str(self.post.title)
    
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk':self.post.pk})
    
    
class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')    
    author = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField( auto_now_add=True)
    
    def __str__(self):
        return self.author + ' | ' + self.text
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.comment.post.pk})
    



class Trending(models.Model):
    title = models.CharField(max_length=100)
    title_tag = models.CharField(max_length=60, null = True, blank = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default = datetime.now, blank= True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name = 'trending_category', default = 'uncategorized')
    image = models.ImageField(null= True, blank = True)
    image2 = models.ImageField(null= True, blank = True)
    body = models.TextField()
    order = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name = 'trending_post')
    class Meta:
        ordering = ['-created_at']
        managed = True
    
    def __str__(self):
        return self.title + ' | ' + str(self.author)
    def get_absolute_url(self):
        return reverse('index')
    def total_likes(self):
        return self.likes.count()
    
    
class Pic(models.Model):
    title = models.CharField(max_length=255)
    title_tag = models.CharField(max_length=60, null = True, blank = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default = datetime.now, blank= True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name = 'pic_category', default = 'uncategorized')
    image = models.ImageField(null= True, blank = True)
    order = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name = 'pic_post')
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title + ' | ' + str(self.author)
    def get_absolute_url(self):
        return reverse('index')
    def total_likes(self):
        return self.likes.count()

   


    
