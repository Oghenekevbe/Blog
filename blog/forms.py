from django import forms 
from .models import Post, Category, Comment, Reply, Pic, Trending, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

choices = Category.objects.all().values_list('name', 'name')
choice_list = []
for item in choices:
    choice_list.append(item)
    
class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ("title","title_tag","image",
                  "author", "category", "body","status", )
        widgets = {
            "title" : forms.TextInput(attrs={'class':'form-control'}),
            "title_tag" : forms.TextInput(attrs={'class':'form-control'}),
            "author" : forms.Select(attrs={'class':'form-control'}), 
            "category" : forms.Select(choices = choice_list,attrs={'class':'form-control'}), 
            "body" : forms.Textarea(attrs={'class':'form-control'}),
            "status" : forms.Select(attrs={'class':'form-control'}),
            "image" : forms.FileInput(attrs={'class':'image_field'}),
        }
        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)
            if user:
                self.fields['author'].queryset = User.objects.filter(pk=user.pk)
        
        
        
class AddCategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ('name', 'description' )
        widgets = {
            "name" : forms.TextInput(attrs={'class':'form-control'}),
            "description" : forms.TextInput(attrs={'class':'form-control'}),
           
        }

class CreateCommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('author', 'text')
        widgets = {
            "author" : forms.TextInput(attrs={'class':'form-control'}),
            "text" : forms.Textarea(attrs={'class':'form-control'}),
        }


class CreateReplyForm(forms.ModelForm):
    
    class Meta:
        model = Reply
        fields = ('author', 'text')
        widgets = {
            "author" : forms.TextInput(attrs={'class':'form-control'}),
            "text" : forms.Textarea(attrs={'class':'form-control'}),
        }



class AddPicForm(forms.ModelForm):
    class Meta:
        model = Pic
        fields = ('title', 'title_tag', 'author', 'category', 'image')
        widgets = {
            "title" : forms.TextInput(attrs={'class':'form-control'}),
            "title_tag" : forms.TextInput(attrs={'class':'form-control'}),
            "author" : forms.Select(attrs={'class':'form-control'}), 
            "category" : forms.Select(choices = choice_list,attrs={'class':'form-control'}), 
            "image" : forms.FileInput(attrs={'class':'image_field'}),
            
        }
        
        
class AddTrendingForm(forms.ModelForm):
    class Meta:
        model = Trending
        fields = ('title', 'title_tag', 'author', 'category', 'body','image', 'image2')
        widgets = {
            "title" : forms.TextInput(attrs={'class':'form-control'}),
            "title_tag" : forms.TextInput(attrs={'class':'form-control'}),
            "author" : forms.Select(attrs={'class':'form-control'}), 
            "category" : forms.Select(choices = choice_list,attrs={'class':'form-control'}), 
            "body" : forms.TextInput(attrs={'class':'form-control'}),
            "image" : forms.FileInput(attrs={'class':'image_field'}),
            
        }


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=255, widget= forms.TextInput(attrs={'class':'form-control'}),required=True,)
    password1 = forms.CharField(max_length=255, widget= forms.PasswordInput(attrs={'class':'form-control', 'type': 'password'}),required=True,)
    password2 = forms.CharField(max_length=255, widget= forms.PasswordInput(attrs={'class':'form-control', 'type': 'password'}),required=True,)
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        
class LoginForm(forms.ModelForm):
    username = forms.CharField(max_length=255, widget= forms.TextInput(attrs={'class':'form-control'}),required=True,)
    password = forms.CharField(max_length=255, widget= forms.PasswordInput(attrs={'class':'form-control', 'type': 'password'}),required=True,)
    
    class Meta:
        model = User
        fields = ('username', 'password')
        
class ChangePassForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=255, widget= forms.PasswordInput(attrs={'class':'form-control', 'type': 'password'}),required=True,)
    new_password1 = forms.CharField(max_length=255, widget= forms.PasswordInput(attrs={'class':'form-control', 'type': 'password'}),required=True,)
    new_password2 = forms.CharField(max_length=255, widget= forms.PasswordInput(attrs={'class':'form-control', 'type': 'password'}),required=True,)
    
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

class EditProfileForm(forms.ModelForm):
        class Meta:
            model = Profile
            fields = ('bio', 'website_url','twitter_url','instagram_url', 'profile_pic')
            widgets = {
                "bio" : forms.TextInput(attrs={'class':'form-control'}),
             
                "twitter_url" : forms.TextInput(attrs={'class':'form-control'}),
                "instagram_url" : forms.TextInput(attrs={'class':'form-control'}),
                "website_url" : forms.TextInput(attrs={'class':'form-control'}),
                "profile_pic" : forms.FileInput(attrs={'class':'image_field'}),
                
            }