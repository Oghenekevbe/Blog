from django.contrib import admin
from .models import Post, Profile,Category, Comment, Reply, Trending, Pic

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    
admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Trending)
admin.site.register(Pic)
admin.site.register(Profile)
    
