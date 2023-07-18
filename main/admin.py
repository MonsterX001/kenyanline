from django.contrib import admin
from .models import Profile, Houseuploads, TimeTracking, Status, Shots, Views, Comment, Comments,FollowingCount, FollowersCount, Podcast, Blogs


# Register your models here.
admin.site.register(Profile)
admin.site.register(Houseuploads)
admin.site.register(Shots)
admin.site.register(Views)
admin.site.register(Comment)
admin.site.register(Comments)
admin.site.register(FollowersCount)
admin.site.register(FollowingCount)
admin.site.register(Podcast)
admin.site.register(Blogs)
admin.site.register(Status)
admin.site.register(TimeTracking)

