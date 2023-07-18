from django.urls import path
from . import views

app_name = 'main'


urlpatterns = [
    path('verify/<str:verification_token>/', views.changepassword, name='verify_email'),

    path('', views.index, name='index'),
    path('podcast/', views.podcast, name='podcast'),
    path('track_time/', views.track_time, name='track_time'),
    path('podcasts/', views.podcasts, name='podcasts'),
    path('blog/', views.blog, name='blog'),
    path('blogs/', views.blogs, name='blogs'),
    path('register/', views.register, name='register'),
    path('share/', views.share_view, name='share'),
    path('recommended', views.Recommended, name='recommended'),
    path('trending', views.trending_posts, name='trending'),
    path('signin', views.signin, name='signin'),
    path('account/<str:pk>', views.account, name='account'),
    path('acc-profile/', views.acc, name='acc'),
    path('logout', views.logout, name='logout'),
    path('Houseupload', views.Houseupload, name='Houseupload'),
    path('search', views.search, name='search'),
    path('Shot', views.Shot, name='Shot'),
    path('shotss', views.shotss, name='shotss'),
    path('livechat', views.livechat, name='livechat'),
    path('terms-policy', views.terms_policy, name='terms-policy'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('hookup', views.hookup, name='hookup'),
    path('socialbook/<str:agentname>/', views.socialbook, name='socialbook'),
    path('video_play/<str:id>', views.video_play, name='video_play'),
    path('podcast_play/<str:id>', views.podcast_play, name='podcast_play'),
    path('blog_read/<str:id>', views.blog_read, name='blog_read'),
    path('forgotpassword', views.forgotpassword, name='forgotpassword'),
    path('changepassword/<token>/', views.changepassword, name='changepassword'),
    path('follow', views.follow, name='follow'),
    path('following', views.following, name='following'),
]