from django.urls import path
from .views import  HomeView, UserRegister,AddPost,EditPost,DeletePost,PostDetail, PostList, AddCategory, CategoryView, CategoryList, LikeView, Comments, CreateComment, CreateReply, Reply, TrendingList, TrendingDetail,PicPreview, PicsDetail, NewTrending, NewPic, EditPic, EditTrend, DeleteTrend, DeletePic, ChangePassword, ShowProfile, EditProfile,YourProfile
from . import views


urlpatterns = [
    path('', HomeView.as_view(), name = 'index'),
    path('post_list/', PostList.as_view(), name = 'post_list'),
    path('add_post/', AddPost.as_view(), name = 'add_post'),
    path('article/edit/<str:pk>', EditPost.as_view(), name = 'edit_post'),
    path('post/<str:pk>/delete', DeletePost.as_view(), name = 'delete_post'),
    path('article/<str:pk>/', PostDetail.as_view(), name = 'post_detail'),
    
    
    #TRENDING NEWS
    path('trending/', TrendingList.as_view(), name = 'trending'),
    path('trending/<str:pk>/', TrendingDetail.as_view(), name = 'trending_detail'),
    path('add_trending/', NewTrending.as_view(), name = 'add_trending'),
    path('trending/edit/<str:pk>/', EditTrend.as_view(), name = 'edit_trend'),
    path('trending/delete/<str:pk>/', DeleteTrend.as_view(), name = 'delete_trend'),
    
    #PIC OF THE DAY
    path('pics/', PicPreview.as_view(), name = 'pics'),
    path('pics/<str:pk>/', PicsDetail.as_view(), name = 'pics_detail'),
    path('add_pic/', NewPic.as_view(), name = 'add_pic'),
    path('pics/edit/<str:pk>/', EditPic.as_view(), name = 'edit_pic'),
    path('pics/delete/<str:pk>/', DeletePic.as_view(), name = 'delete_pic'),

    
    #CATEGORIES   
    path('add_category/', AddCategory.as_view(), name = 'add_category'),
    path('categories/<str:cats>/', CategoryView.as_view(), name = 'categories'), #this shows posts for each category queried
    path('category_list/', CategoryList.as_view(), name = 'category_list'), 
    
    
    #USER INTERACTIONS   
    path('like/<str:pk>/', views.LikeView, name = 'like_post'),
    path('article/<str:pk>/comments/new/', CreateComment.as_view(), name = 'create_comment'),
    path('article/<str:pk>/comments/', Comments.as_view(), name='comments'),    
    path('article/<str:pk>/comments/<str:comment_pk>/replies/new/', CreateReply.as_view(), name='create_reply'),
    path('article/<str:pk>/comments/<str:comment_pk>/replies/', Reply.as_view(), name='replies'),    
    
    #USER CREDENTIALS
    path('register/', UserRegister.as_view(), name = 'register'),
    path('password/',ChangePassword.as_view(template_name='registration/change-password.html'), name='password' ),
    path('<str:pk>/profile', ShowProfile.as_view(), name='author_profile' ),
    path('<str:pk>/your_profile/', YourProfile.as_view(), name = 'your_profile'),
    path('<str:pk>/edit_profile', EditProfile.as_view(), name='edit_profile' ),
    path('unauthorized', views.unauthorized, name='unauthorized' ),
    
    

]