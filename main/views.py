from django.shortcuts import render, redirect, render, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Houseuploads, TimeTracking, Shots, User, Status, Views, Comment, Comments, Blogcomment, FollowersCount, FollowingCount, Share, Podcast, Blogs
from .filters import ListingFilter
from django.core.paginator import Paginator
from django.urls import reverse
import uuid
from .helpers import send_forgetpassword_mail
from django.db.models import Q
from itertools import chain
from django.utils import timezone
from datetime import timedelta
from .utills import generate_verification_token, send_verification_email
from itertools import groupby
from operator import itemgetter
from django.shortcuts import render
from itertools import groupby
from operator import itemgetter
from django.views.decorators.csrf import csrf_exempt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



# Create your views here.
@login_required(login_url='/signin')
def index(request):
    user_profile = Profile.objects.filter(user=request.user)
    listings = Houseuploads.objects.all()
    user_posts = Houseuploads.objects.filter(user=request.user)
    listing_filter = ListingFilter(request.GET, queryset = listings)
    follower = request.user  # Assuming the follower is the currently logged-in user
    followed_users = FollowersCount.objects.filter(follower=follower)
    followed_users_len = followed_users.count()
        
    #set pagination
    #X = user_posts()

    p = Paginator(Houseuploads.objects.all(), 9)
    page = request.GET.get('page')
    venues = p.get_page(page)

    context ={
        'followed_users': followed_users_len,
        'listing_filter': listing_filter,
        'listings': listings,
        'venues' : venues,
        'user_profile' :user_profile,
        'user_post' :user_posts,
    }

    return render(request, 'index.html',  context)

@login_required(login_url='/signin')
def Recommended(request):
    user_profile = Profile.objects.filter(user=request.user)

    user_following_list = []
    feed = []
    feeds = []
    feedz = []
    user_following = FollowersCount.objects.filter(follower=request.user.username)
    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Houseuploads.objects.filter(user=usernames)
        feed_listss = Podcast.objects.filter(user=usernames)
        feed_listz = Blogs.objects.filter(user=usernames)
        feed.append(feed_lists)
        feeds.append(feed_listss)
        feedz.append(feed_listz)

    feed_lists = list(chain(*feed))
    feed_listss = list(chain(*feeds))
    feed_listz = list(chain(*feedz))

    follower = request.user  # Assuming the follower is the currently logged-in user
    followed_users = FollowersCount.objects.filter(follower=follower)
    followed_users_len = followed_users.count()
    context = {
        'followed_users': followed_users_len,
        'feed_lists':feed_lists,
        'feed_listss':feed_listss,
        'feed_listz':feed_listz,
        'user_profile' :user_profile,
        'user_following':user_following_list
    }

    return render(request, 'recommended.html',  context)




def generate_recommendations(username):
    # Retrieve user's videos or content based on the username
    user_videos = Status.objects.filter(user=username)

    # Generate recommendations based on the user's videos
    recommendations = []

    # Implement your recommendation logic here
    # Example recommendation logic:
    recommended_videos = Status.objects.exclude(user=username)[:5]

    # Append recommended videos to the recommendations list
    recommendations.extend(recommended_videos)

    return recommendations

def Recommend(request):
    user_following_list = []
    feed = []
    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for username in user_following_list:
        # Generate individual recommendations for each user
        user_recommendations = generate_recommendations(username)
        feed.extend(user_recommendations)

    # Group the feed by username
    feed.sort(key=itemgetter('user'))
    grouped_feed = groupby(feed, key=itemgetter('user'))

    context = {
        'grouped_feed': grouped_feed,
        'user_following': user_following_list
    }

    return render(request, 'recommend.html', context)



def trending_posts(request):
    user_profile = Profile.objects.filter(user=request.user)
    follower = request.user  # Assuming the follower is the currently logged-in user
    followed_users = FollowersCount.objects.filter(follower=follower)
    followed_users_len = followed_users.count()
        
    # Calculate the date one week ago
    one_week_ago = timezone.now() - timedelta(weeks=1)

    # Fetch the trending posts based on views in the last week
    trending_posts = Houseuploads.objects.filter(created_at__gte=one_week_ago).order_by('-no_of_views')[:10]
    trending_blogs = Blogs.objects.filter(created_at__gte=one_week_ago).order_by('-no_of_views')[:10]
    trending_podcast = Podcast.objects.filter(created_at__gte=one_week_ago).order_by('-no_of_views')[:10]
    

    context={
        'trending_posts': trending_posts,
        'trending_blogs': trending_blogs,
        'trending_podcast': trending_podcast,
        'user_profile' :user_profile,
        'followed_users' :followed_users_len,
    }

    return render(request, 'trending.html', context)

@login_required(login_url='/signin')
def share_view(request):
    if request.method == 'POST':
        user = request.user
        shared_link = request.POST['shared_link']
        Share.objects.create(user=user, shared_link=shared_link)
        # Redirect to a success page or the shared link's page
        return redirect('success-page')

    # Handle GET requests or render the share form
    return render(request, 'base.html')

def share_view(request):
    # Retrieve the Share object
    share = Share.objects.first()

    # Increment the share_count
    share.share_count += 1
    share.save()
    context = {
        'share_count': share.share_count,
    }
    # Redirect the user to the desired page after sharing
    
    return render(request, 'target_page.html', context)

@login_required(login_url='/signin')
def link_detail_view(request, link_id):
    shared_link = Share.objects.filter(user=request.user, shared_link=link_id).count()
    context = {'shared_link': shared_link}
    return render(request, 'account.html', context)

@login_required(login_url='/signin')
def shotss(request):
 
        #user_profile = Profile.objects.get(user=request.user)
        listings = Shots.objects.all()
        user_posts = Shots.objects.filter(user=request.user)
        listing_filter = ListingFilter(request.GET, queryset = listings)
        
        #set pagination
        #X = user_posts()

        p = Paginator(Shots.objects.all(), 20)
        page = request.GET.get('page')
        venues = p.get_page(page)

        context ={
            'listing_filter': listing_filter,
            'listings': listings,
            'venues' : venues,
            #'user_profile' :user_profile,
            'user_post' :user_posts,
        }

        return render(request, 'shotvideos.html',  context)

@login_required(login_url='/signin')
def hookup(request):
    user_profile = Profile.objects.filter(user=request.user)
    user_profiles = Profile.objects.all()
    follower = request.user  # Assuming the follower is the currently logged-in user
    followed_users = FollowersCount.objects.filter(follower=follower)
    followed_users_len = followed_users.count()
        
    context ={
        'user_profiles':user_profiles,
        'user_profile':user_profile,
        'followed_users':followed_users_len
    }

    return render(request, 'hookups.html', context)

def socialbook(request, agentname):
    profile = get_object_or_404(Profile, agentname=agentname)
    user_object = User.objects.get(username=agentname)
    user_profile = Profile.objects.get(user=user_object)

    user_posts = Houseuploads.objects.filter(user=agentname)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = agentname

    if FollowingCount.objects.filter(follower=follower, user=user).first():
        button_text = 'UNFOLLOW'

    else:
        button_text = 'FOLLOW'

    user_followers = len(FollowingCount.objects.filter(user=agentname))
    
    context = {
        'profile':profile,
        'user_object':user_object,
        'user_profile':user_profile,
        'user_posts':user_posts,
        'user_post_length':user_post_length,
        'button_text':button_text,
        'user_followers': user_followers,

    }

    return render(request, 'socialbook.html', context)

@login_required(login_url='/signin')
def livechat(request):
    user_profile = Profile.objects.filter(user=request.user) 
    follower = request.user  # Assuming the follower is the currently logged-in user
    followed_users = FollowersCount.objects.filter(follower=follower)
    followed_users_len = followed_users.count()
        
    context={
        'user_profile':user_profile,
        'followed_users':followed_users_len,
    } 
    return render(request, 'livechat.html', context)
def terms_policy(request):
    
    return render(request, 'termspolicy.html')

@login_required(login_url='/signin')

def search(request):
    user_profile = Profile.objects.filter(user=request.user)
    follower = request.user  # Assuming the follower is the currently logged-in user
    followed_users = FollowersCount.objects.filter(follower=follower)
    followed_users_len = followed_users.count()
        
    context = {
        'user_profile': user_profile,
        'followed_users': followed_users_len,
    }

    if request.method == "POST":
        searched = request.POST.get('searched', '').strip()
        if searched:
            results = search_database(searched)
            resultsone = search_databaseone(searched)
            resultstwo = search_databasetwo(searched)
            resultsthree = search_databasethree(searched)
            resultsfour = search_databasefour(searched)

            context.update({
                'searched': searched,
                'videos': results,
                'videosone': resultsone,
                'videostwo': resultstwo,
                'videosthree': resultsthree,
                'videosfour': resultsfour,
            })

            if not any([results, resultsone, resultstwo, resultsthree, resultsfour]):
                context['no_results_message'] = 'Your search was not found.'
        else:
            context['empty_search_message'] = 'You did not search for anything.'

    return render(request, 'searches.html', context)


def search_database(query):
    # Perform the search query across multiple models
    results = []

    # Calculate the threshold for resemblance
    threshold = int(len(query) * 0.6)

    # Search in Houseuploads
    houseuploads_results = Houseuploads.objects.filter(Q(details__icontains=query[:threshold]) | Q(user__icontains=query[:threshold]) | Q(Video_name__icontains=query[:threshold]))
    results.extend(houseuploads_results)

    return results
def search_databaseone(query):
    # Perform the search query across multiple models
    resultsone = []

    # Calculate the threshold for resemblance
    threshold = int(len(query) * 0.6)

    # Search in Podcast
    podcast_results = Podcast.objects.filter(Q(details__icontains=query[:threshold]) | Q(user__icontains=query[:threshold]) | Q(Video_name__icontains=query[:threshold]))
    resultsone.extend(podcast_results)

    return resultsone
def search_databasetwo(query):
    # Perform the search query across multiple models
    resultstwo = []

    # Calculate the threshold for resemblance
    threshold = int(len(query) * 0.6)

    # Search in Blogs
    blogs_results = Shots.objects.filter(Q(details__icontains=query[:threshold]) | Q(user__icontains=query[:threshold]) | Q(Video_name__icontains=query[:threshold]))
    resultstwo.extend(blogs_results)
def search_databasethree(query):
    # Perform the search query across multiple models
    resultsthree = []

    # Calculate the threshold for resemblance
    threshold = int(len(query) * 0.6)

    # Search in Blogs
    blogs_results = Blogs.objects.filter(Q(details__icontains=query[:threshold]) | Q(user__icontains=query[:threshold]) | Q(Video_name__icontains=query[:threshold]))
    resultsthree.extend(blogs_results)

    return resultsthree
def search_databasefour(query):
    # Perform the search query across multiple models
    resultsfour = []

    # Calculate the threshold for resemblance
    threshold = int(len(query) * 0.6)

    # Search in Blogs
    blogs_results = Profile.objects.filter(Q(agentname__icontains=query[:threshold]) | Q(bio__icontains=query[:threshold]) | Q(location__icontains=query[:threshold]))
    resultsfour.extend(blogs_results)

    return resultsfour

@login_required(login_url='/signin') 

       
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('/register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('/register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                #verification_token = generate_verification_token(user)
                #send_verification_email(user, verification_token)
                #log user and redirect to uploading page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login) 
                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect ('/acc-profile')
        else:
            messages.info(request, 'Passwords not matching')
            return redirect('/register')
    else:
        return render(request, 'register.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Are Invalid')
            return redirect('/signin')
    else:
        return render(request, 'signin.html')


@login_required(login_url='/signin')
def account(request, pk):
   
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Houseuploads.objects.filter(user=pk)
    user_podcasts = Podcast.objects.filter(user=pk)
    user_blogs = Blogs.objects.filter(user=pk)
    user_shots = Shots.objects.filter(user=pk)
    user_followers = len(FollowersCount.objects.filter(user=pk))
    follower = request.user  # Assuming the follower is the currently logged-in user
    followed_users = FollowersCount.objects.filter(follower=follower)
    followed_users_len = followed_users.count()
        
    calculated_values = []
    for x in user_posts:
        y = x.no_of_views
        z = round(y * 0.3, 2)  # Round to 2 decimal places

        calculated_values.append(z)

    calculated_valuesy = []
    for y in user_podcasts:
        a = y.no_of_views
        b = round(a * 0.3, 2)  # Round to 2 decimal places

        calculated_valuesy.append(b)

    calculated_valuesz = []
    for z in user_blogs:
        c = z.no_of_views
        d = round(c * 0.3, 2)  # Round to 2 decimal places

        calculated_valuesz.append(d)

    total = round(sum(calculated_values + calculated_valuesy + calculated_valuesz), 2)  # Round the total to 2 decimal places


    context = {
        'user_object':user_object,
        'user_profile':user_profile,
        'user_posts':user_posts,
        'user_podcasts':user_podcasts,
        'user_blogs':user_blogs,
        'user_shots':user_shots,
        'calculated_values':calculated_values,
        'calculated_valuesy':calculated_valuesy,
        'calculated_valuesz':calculated_valuesz,
        'user_followers':user_followers,
        'followed_users':followed_users_len,
        'total':total
    }


    return render(request, 'account.html', context)

@login_required
@csrf_exempt
def track_time(request):
    if request.method == 'POST':
        time_spent = int(request.POST.get('time_spent'))
        try:
            time_tracking = TimeTracking.objects.get(user=request.user)
            time_tracking.time_spent += time_spent
            time_tracking.save()
        except TimeTracking.DoesNotExist:
            TimeTracking.objects.create(user=request.user, time_spent=time_spent)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

@login_required(login_url='/signin')
def podcast(request):
    user_profile = Profile.objects.filter(user=request.user)
    follower = request.user  # Assuming the follower is the currently logged-in user
    followed_users = FollowersCount.objects.filter(follower=follower)
    followed_users_len = followed_users.count()
        
    context={
        'user_profile':user_profile,
        'followed_users':followed_users_len,
    }
    if request.method == 'POST':
        
        user = request.user.username
        video_name = request.POST['housename']
        main_img = request.FILES.get('mainimg')
        details = request.POST['details']
        
        new_post =  Podcast.objects.create(user = user, Video_name=video_name, main_img=main_img, details=details) 
        new_post.save() 
        return redirect('/acc-profile')
    
    
    return render(request, 'podupload.html', context)

@login_required(login_url='/signin')
def blog(request):

    user_profile = Profile.objects.filter(user=request.user)
    follower = request.user  # Assuming the follower is the currently logged-in user
    followed_users = FollowersCount.objects.filter(follower=follower)
    followed_users_len = followed_users.count()
        
    context={
        'user_profile':user_profile,
        'followed_users':followed_users_len,
    }
    if request.method == 'POST':
        
        user = request.user.username
        video_name = request.POST['housename']
        main_img = request.FILES.get('mainimg')
        details = request.POST['details']
        
        new_post =  Blogs.objects.create(user = user, Video_name=video_name, main_img=main_img, details=details) 
        new_post.save() 
        return redirect('/blogs')
    
    
    return render(request, 'blogs.html', context)



@login_required(login_url='/signin')

def podcasts(request):
    user_profile = Profile.objects.filter(user=request.user)
    listings = Podcast.objects.all()
    user_posts = Podcast.objects.filter(user=request.user)
    listing_filter = ListingFilter(request.GET, queryset = listings)
    follower = request.user  # Assuming the follower is the currently logged-in user
    followed_users = FollowersCount.objects.filter(follower=follower)
    followed_users_len = followed_users.count()
        
    #set pagination
    #X = user_posts()

    p = Paginator(Podcast.objects.all(), 9)
    page = request.GET.get('page')
    venues = p.get_page(page)

    context ={
        'listing_filter': listing_filter,
        'listings': listings,
        'venues' : venues,
        'user_profile' :user_profile,
        'user_post' :user_posts,
        'followed_users':followed_users_len
    }

    return render(request, 'podcast.html',  context)

@login_required(login_url='/signin')
def blogs(request):
    user_profile = Profile.objects.filter(user=request.user)
    listings = Blogs.objects.all()
    user_posts = Blogs.objects.filter(user=request.user)
    listing_filter = ListingFilter(request.GET, queryset = listings)
    
    #set pagination
    #X = user_posts()

    p = Paginator(Blogs.objects.all(), 9)
    page = request.GET.get('page')
    venues = p.get_page(page)

    context ={
        'listing_filter': listing_filter,
        'listings': listings,
        'venues' : venues,
        'user_profile' :user_profile,
        'user_post' :user_posts,
    }

    return render(request, 'blogss.html',  context)

@login_required(login_url='/signin')
def blog_read(request, id):
    user_profile = Profile.objects.filter(user=request.user)
    posts = Blogs.objects.filter(id = id)
    blogs = get_object_or_404(Blogs, pk=id)
    blogcomment = Blogcomment.objects.filter(blogs=blogs)
    

    if request.method == 'POST':
        text = request.POST['text']
        blogcomments = Blogcomment(user=request.user, blogs=blogs, text=text)
        blogcomments.save()

    user_post_length = len(blogcomment)

    
    blogs = Blogs.objects.get(id=id)
    related_blogs = Blogs.objects.filter(details__icontains=blogs.details).exclude(id=id)[:5]  # Example: get videos with similar titles, excluding the current video
    context={
        'posts':posts,
        'blogs': blogs,
        'blogcomment':  blogcomment,
        'user_post_length': user_post_length,
        'related_blogs': related_blogs,
        'user_profile': user_profile
    }
    username = request.user.username


    post = Blogs.objects.get( id = id)

    like_filter = Views.objects.filter(post_Id=id, username=username).first()

    if like_filter == None:
        new_view = Views.objects.create(post_Id=id, username=username)
        new_view.save()
        post.no_of_views = post.no_of_views + 1
        post.save()
    else:
        post.no_of_views = post.no_of_views 
        post.save()     

    return render(request, 'blog_read.html',  context)




@login_required(login_url='/signin')
def acc(request):
    user_posts = Houseuploads.objects.filter(user=request.user)
    user_profile = Profile.objects.get(user=request.user)
        
    context={
        'user_posts':user_posts,
        'user_profile': user_profile,
    }
    
    if request.method == 'POST' and 'profile_submit' in request.POST:
       
            profileimg = request.FILES.get('image')
            profileimg1 = request.FILES.get('image1')
            profileimg2 = request.FILES.get('image2')
            profileimg3 = request.FILES.get('image3')
            profileimg4 = request.FILES.get('image4')
            profileimg5 = request.FILES.get('image5')
            profileimg6 = request.FILES.get('image6')
            agentname = request.POST['agencyname']
            location = request.POST['location']
            bio =request.POST['agentdetails']

            user_profile.profileimg = profileimg
            user_profile.main_img1 = profileimg1
            user_profile.main_img2 = profileimg2
            user_profile.main_img3 = profileimg3
            user_profile.main_img4 = profileimg4
            user_profile.main_img5 = profileimg5
            user_profile.main_img6 = profileimg6
            user_profile.agentname = agentname
            user_profile.location = location
            user_profile.bio = bio 
            user_profile.save()      

            return redirect('/acc-profile')

    else: 
        user_profile.refresh_from_db()      
        

        return render(request, 'acc-profile.html', context)


@login_required(login_url='/signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    house_posts = Houseuploads.objects.filter(user=pk)
    shot_posts = Shots.objects.filter(user=pk)
    podcast_posts = Podcast.objects.filter(user=pk)
    blog_posts = Blogs.objects.filter(user=pk)

    house_posts_length = len(house_posts)
    shot_posts_length = len(shot_posts)
    podcast_posts_length = len(podcast_posts)
    blog_posts_length = len(blog_posts)

    combined_length = (
        house_posts_length +
        shot_posts_length +
        podcast_posts_length +
        blog_posts_length
    )

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'UNSUBSCRIBE'

    else:
        button_text = 'SUBSCRIBE'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowingCount.objects.filter(user=pk))
    
    context = {
        'user_object':user_object,
        'user_profile':user_profile,
        'combined_length':combined_length,
        'button_text':button_text,
        'user_followers': user_followers,
        'user_following': user_following,
        'house_posts_length': house_posts,
        'podcast_posts_length': podcast_posts,
        'shot_length': shot_posts,
        'blog_posts_length': blog_posts,

    }
    return render(request, 'profile.html', context)
    


@login_required(login_url='/signin')
def Houseupload(request):
    user_profile = Profile.objects.filter(user=request.user)
    follower = request.user  # Assuming the follower is the currently logged-in user
    followed_users = FollowersCount.objects.filter(follower=follower)
    followed_users_len = followed_users.count()
        
    context ={
        'user_profile':user_profile,
        'followed_users':followed_users_len
    }
    if request.method == 'POST':
        
        user = request.user.username
        video_name = request.POST['housename']
        main_img = request.FILES.get('mainimg')
        details = request.POST['details']
        
        new_post =  Houseuploads.objects.create(user = user, Video_name=video_name, main_img=main_img, details=details) 
        new_post.save() 
        return redirect('/acc-profile')
    
    
    return render(request, 'houseuploads.html', context)
@login_required(login_url='/signin')
def Shot(request):
    user_profile = Profile.objects.filter(user=request.user)
    follower = request.user  # Assuming the follower is the currently logged-in user
    followed_users = FollowersCount.objects.filter(follower=follower)
    followed_users_len = followed_users.count()
        
    context={
        'user_profile':user_profile,
        'followed_users':followed_users_len
    }
    if request.method == 'POST':
        
        user = request.user.username
        video_name = request.POST['housename']
        main_img = request.FILES.get('mainimg')
        details = request.POST['details']


        new_post =  Shots.objects.create(user = user, Video_name=video_name, main_img=main_img, details=details) 
        new_post.save()
        return redirect('/acc-profile')
    
    
    return render(request, 'shots.html', context)
    

def video_play(request, id):
    user_profile = Profile.objects.filter(user=request.user)
    posts = Houseuploads.objects.filter(id = id)
    video = get_object_or_404(Houseuploads, pk=id)
    comments = Comment.objects.filter(video=video)
    

    if request.method == 'POST':
        text = request.POST['text']
        comment = Comment(user=request.user, video=video, text=text)
        comment.save()

    user_post_length = len(comments)


    blogs = Houseuploads.objects.get(id=id)
    related_videos = Blogs.objects.filter(details__icontains=blogs.details).exclude(id=id)[:5]  # Example: get videos with similar titles, excluding the current video
    context={
        'posts':posts,
        'video': video,
        'comments': comments,
        'user_post_length': user_post_length,
        'related_videos': related_videos,
        'user_profile': user_profile
    }
    username = request.user.username


    post = Houseuploads.objects.get( id = id)

    like_filter = Views.objects.filter(post_Id=id, username=username).first()

    if like_filter == None:
        new_view = Views.objects.create(post_Id=id, username=username)
        new_view.save()
        post.no_of_views = post.no_of_views + 1
        post.save()
    else:
        post.no_of_views = post.no_of_views 
        post.save()     
    return render(request, 'video_play.html', context)

def podcast_play(request, id):
    user_profile = Profile.objects.filter(user=request.user)
    posts = Podcast.objects.filter(id = id)
    videos = get_object_or_404(Podcast, pk=id)
    commentss = Comments.objects.filter(videos=videos)
    

    if request.method == 'POST':
        texts = request.POST['text']
        comments = Comments(user=request.user, videos=videos, texts=texts)
        comments.save()

    user_post_length = len(commentss)
    videos = Podcast.objects.get(id=id)
    related_videos = Podcast.objects.filter(details__contains=videos.details).exclude(id=id)[:5]  # Example: get videos with similar titles, excluding the current video

    context={
        'posts':posts,
        'videos': videos,
        'video': videos,
        'user_profile': user_profile,
        'commentss': commentss,
        'user_post_length': user_post_length,
        'related_videos': related_videos
    }
    username = request.user.username


    post = Podcast.objects.get( id = id)

    like_filter = Views.objects.filter(post_Id=id, username=username).first()

    if like_filter == None:
        new_view = Views.objects.create(post_Id=id, username=username)
        new_view.save()
        post.no_of_views = post.no_of_views + 1
        post.save()
    else:
        post.no_of_views = post.no_of_views 
        post.save()     
    return render(request, 'podcast_play.html', context)


def changepassword(request , token):
    
    try:
        profile_obj = Profile.objects.filter(forget_password_token = token).first()
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_pasword = request.POST.get('confirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'user id not found')
                return redirect('/changepassword/{token}')

            if new_password != confirm_pasword:
                messages.success(request, 'Passwords not matching')
                return redirect('/changepassword/{token}')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save
            return redirect('/signin')
        
        #context={'user_id' : profile_obj.user.id}

    except Exception as e:
        print(e)
    return render(request, 'changepassword.html')


def forgotpassword(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('username')

            if not User.objects.filter(email=email).first():
                messages.success(request, 'That email adress does not exist')
                return redirect('/forgotpassword')

            user_obj = User.objects.get(email=email)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()

            send_forgetpassword_mail(user_obj.email, token)
            messages.success(request, 'An Email has been sent, click on the link to reset password')
            return redirect('/forgotpassword')

    except Exception as e:
        print(e)    
    return render(request, 'forgotpassword.html')

@login_required(login_url='/signin')
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect ('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')
    
@login_required
def following(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowingCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowingCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect ('/socialbook/'+user)
        else:
            new_follower = FollowingCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/socialbook/'+user)
    else:
        return redirect('/')
    
