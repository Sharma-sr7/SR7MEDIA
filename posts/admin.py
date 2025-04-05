from django.contrib import admin
from .models import Post,LikePost,FollowersCount,Comment,DeletedUsers

admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
admin.site.register(Comment)
admin.site.register(DeletedUsers)