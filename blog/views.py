from django.shortcuts import render,redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import Post, Category, Comment, Reply, Trending, Pic, Profile
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy,reverse
from django.http import  HttpResponseRedirect
from .forms import PostForm, AddCategoryForm, CreateCommentForm, CreateReplyForm, AddTrendingForm, AddPicForm,ChangePassForm, EditProfileForm, RegisterForm
from django.http import Http404
import random


# Create your views here.

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('unauthorized')

'''
Views written on this page
- trending views
- pic of the day views
- blog views
- views for user interactions (likes & comments)
- views for user credentials e.g register, etc

'''

''' Trending Views '''
class TrendingList(ListView):
    model = Trending
    template_name = 'trending.html'
    context_object_name = 'Trends'
    def get_queryset(self):
        return self.model.objects.all().order_by('-created_at')
    
    
class TrendingDetail(DetailView):
    model = Trending
    template_name = 'trending_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trending"] = self.object
        context["total_likes"] = self.object.total_likes()
        return context
    
    
class NewTrending(CreateView):
    model = Trending
    template_name = 'add_trending.html'
    form_class = AddTrendingForm
    
class EditTrend(StaffRequiredMixin,UpdateView):
    model = Trending
    template_name = 'edit_trend.html'
    form_class = AddTrendingForm
    
class DeleteTrend(StaffRequiredMixin,DeleteView):
    model = Trending
    template_name = 'delete_trend.html'
    success_url = reverse_lazy('index')
        
    
'''pic of the day views'''
class PicPreview(ListView):
    model = Pic
    template_name = 'pics.html'
    context_object_name = 'potd'
    def get_queryset(self):
        return self.model.objects.all().order_by('-created_at')
    
class PicsDetail(DetailView):
    model = Pic
    template_name = 'pics_detail.html'

    def get_context_data(self,*args, **kwargs):
        context = super(PicsDetail,self).get_context_data(*args,**kwargs)
        likes_count = get_object_or_404(Pic, id = self.kwargs['pk'])
        total_likes = likes_count.total_likes() #it was created in the model
        context["total_likes"] = total_likes 
        return context
    
class NewPic(CreateView):
    model = Pic
    template_name = 'add_pic.html'
    form_class = AddPicForm
    
class EditPic(StaffRequiredMixin,UpdateView):
    model = Pic
    template_name = 'Edit_pic.html'
    form_class = AddPicForm
    def after_edit(request):
        return redirect('pics.html')


class DeletePic(StaffRequiredMixin,DeleteView):
    model = Pic
    template_name = 'delete_pic.html'
    success_url = reverse_lazy('index')
    
    
    







''' Blog views '''

class HomeView(ListView):
    model = Post
    context_object_name = 'Post'
    template_name = 'index.html'
   
    def get_queryset(self):
        return self.model.objects.all().order_by('-created_at')
    
    def get_trending(self):
        return Trending.objects.all()
    
    def get_pic(self):
        return Pic.objects.all()
    
    def get_random_pic(self):
        pics = Pic.objects.all()
        if pics:
            return random.choice(pics)
        else:
            return None
    
    
    def get_context_data(self, *args,**kwargs):
        cat_menu = Category.objects.all()
        trending = self.get_trending()
        pics =self.get_pic()
        random_pic = self.get_random_pic()
        
        context = super(HomeView,self).get_context_data(*args,**kwargs)
        context["cat_menu"] = cat_menu
        context["trending"] = trending
        context["pics"] = pics
        context["random_pic"] = random_pic
        return context
        
class PostList(ListView):
    model = Post
    context_object_name = 'Post'
    template_name = 'post_list.html'
    def get_queryset(self):
        return self.model.objects.all().order_by('-created_at')
    
class AddPost(StaffRequiredMixin,CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('index')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['author'].initial = self.request.user
        return form

class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self,*args, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context["post"] = self.object
        context["total_likes"] = self.object.total_likes()
        return context
    



    

class EditPost(StaffRequiredMixin,UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'edit_post.html'
            
class DeletePost(StaffRequiredMixin, DeleteView):
    model = Post
    template_name = 'delete_post.html'
    form_class = PostForm
    success_url = reverse_lazy('index')
    
class AddCategory(StaffRequiredMixin,CreateView):
    model = Category
    form_class = AddCategoryForm
    template_name = 'add_category.html'
    
    

class CategoryView(ListView):
    model = Category
    template_name = 'categories.html'

    def get_pics(self):
        cats = self.kwargs['cats']
        category = Category.objects.get(name=cats)
        return Pic.objects.filter(category=category)

    def get_trend(self):
        cats = self.kwargs['cats']
        category = Category.objects.get(name=cats)
        return Trending.objects.filter(category=category)

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryView, self).get_context_data(*args, **kwargs)
        cats = self.kwargs['cats']
        category_post = Category.objects.filter(name=cats)
        category_pic = self.get_pics()
        category_trend = self.get_trend()
        context["category_post"] = category_post
        context["category_pic"] = category_pic
        context["category_trend"] = category_trend
        return context


class CategoryList(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'category_list.html'
    def get_context_data(self, *args,**kwargs):
        cat_menu = Category.objects.all()
        context = super(CategoryList,self).get_context_data(*args,**kwargs)
        context["cat_menu"] = cat_menu
        return context
    
    
    
''' views for user interactions (LIKES & COMMENT)'''
    
# def LikeView(request,pk):
#     post = get_object_or_404(Post, id=request.POST.get('post_id'))
#     post.likes.add(request.user)
#     return HttpResponseRedirect(reverse('post_detail', args=[str(pk)] ))

def LikeView(request, pk):
    model_name = request.POST.get('model_name')
    if model_name == 'pic':
        obj = get_object_or_404(Pic, id=pk)
        view_name = 'pics_detail'
    elif model_name == 'post':
        obj = get_object_or_404(Post, id=pk)
        view_name = 'post_detail'
    elif model_name == 'trend':
        obj = get_object_or_404(Trending, id=pk)
        view_name = 'trending_detail'
    else:
        return render(request,'404.html', status=404)
    obj.likes.add(request.user)
    return HttpResponseRedirect(reverse(view_name, args=[pk]))

    

class CreateComment(LoginRequiredMixin,CreateView):
    model = Comment
    form_class = CreateCommentForm
    template_name = 'create_comment.html'
    def form_valid(self,form):
        form.instance.post_id = self.kwargs['pk']
        response =  super(CreateComment, self).form_valid(form)
        return redirect(self.object.get_absolute_url())  
    
    
class Comments(ListView):
    model = Comment
    template_name = 'comments.html'
    context_object_name = 'comments'
    
    
    

class CreateReply(LoginRequiredMixin,CreateView):
    model = Reply
    form_class = CreateReplyForm
    template_name = 'create_reply.html'

    def form_valid(self, form):
        form.instance.comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        response = super().form_valid(form)
        return redirect(self.object.get_absolute_url())  


class Reply(ListView):
    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['comment_pk'])
        replies = Reply.objects.filter(comment=comment)
        return render(request, 'replies.html', {'replies': replies})
 
       
       

    
    
 
 
 
 
 
    
''' views for user credentials'''
    
class UserRegister(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class ChangePassword(PasswordChangeView):
    form_class = ChangePassForm
    success_url = reverse_lazy('index')

class ShowProfile(DetailView):
    model = Profile
    template_name = 'registration/author_profile.html'
    
    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(ShowProfile,self).get_context_data(*args, **kwargs)

        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])

        context["page_user"] = page_user
        

        return context
    
class YourProfile(DetailView):
    model = Profile
    template_name = 'registration/your_profile.html'
    def get_context_data(self, *args, **kwargs):
        context = super(YourProfile,self).get_context_data(*args, **kwargs)
        page_user = Profile.objects.get(user=self.request.user)
        context["page_user"] = page_user
        return context

    
    

    
class EditProfile(UpdateView):
    model = Profile
    template_name = 'registration/edit_profile.html'
    form_class = EditProfileForm
    
    def get_object(self, queryset=None):
        profile = super().get_object(queryset=queryset)
        if profile.user.id != self.request.user.id:
            raise PermissionDenied
        return profile
    
    success_url = '/'

@user_passes_test(lambda u: u.is_supervisor)
def SuperUserAdmin(request):
    return redirect('admin:index')


def unauthorized(request):
    return render(request, 'registration/unauthorized.html')