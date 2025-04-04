from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from users.models import Profile
from .models import Post,LikePost,FollowersCount,Comment,DeletedUsers
from django.contrib.auth.models import User
from itertools import chain
from django.http import JsonResponse
from django.contrib import messages



@login_required(login_url='login_url')
def Home(request):
    user_profile = Profile.objects.get(user=request.user)
    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    for post in feed_list:
        post.is_liked_by_user = LikePost.objects.filter(post_id=post.id, username=request.user.username).exists()
        post.like_count = LikePost.objects.filter(post_id=post.id).count()
        post.comment_count = Comment.objects.filter(post=post).count()

    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestion_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)

    final_suggetions_list = [x for x in list(new_suggestion_list) if (x not in list(current_user))]
    username_profile = []
    username_profile_list = []

    for users in final_suggetions_list:
        username_profile.append(users.id)

    for id in username_profile:
        profile_lists = Profile.objects.filter(id_user=id)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(request,'index.html',{"user_profile":user_profile,'posts':feed_list,'suggestions_username_profile_list':suggestions_username_profile_list})

@login_required(login_url='login_url')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=request.user)
    other_user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_posts_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower,user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))
    return render(request,'profile.html',{"user_profile":user_profile,'user_object':user_object,'other_user_profile':other_user_profile ,'user_posts':user_posts,'user_posts_length':user_posts_length,'button_text':button_text,'user_followers':user_followers,'user_following':user_following})

@login_required(login_url='login_url')
def update(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        if request.FILES.get('profile') == None:
            image =user_profile.profileimg
            bio = request.POST['bio']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.save()

        if request.FILES.get('profile') != None:
            image =request.FILES.get('profile')
            bio = request.POST['bio']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.save()
        return redirect('profile_url' , pk=user_profile)

    
    return render(request,'settings.html',{"user_profile":user_profile})

@login_required(login_url='login_url')
def upload(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        user = request.user.username
        user_image = user_profile.profileimg
        image = request.FILES.get('image')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user,user_image=user_image,image=image,caption=caption,)
        new_post.save()
        return redirect('profile_url' , pk=user_profile)
        
    return render(request,'upload.html',{"user_profile":user_profile})

@login_required(login_url='login_url')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)
    like_filter = LikePost.objects.filter(post_id=post_id,username=username).first()

    if like_filter is None:
        LikePost.objects.create(post_id=post_id, username=username)
        liked = True
    else:
        like_filter.delete()
        liked = False

    like_count = LikePost.objects.filter(post_id=post_id).count()

    return JsonResponse({"likes": like_count, "liked": liked})
    
@login_required(login_url='login_url')
def follow(request):
    if request.method == "POST":
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower,user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect('profile_url',pk=user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect('profile_url',pk=user)

@login_required(login_url='login_url')
def search(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains = username)
        username_profile =[]
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for id in username_profile:
            profile_lists = Profile.objects.filter(id_user = id)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
    return render(request,'search.html',{"user_profile":user_profile,'username_profile_list':username_profile_list,'username':username})

@login_required(login_url='login_url')
def privacy(request):
    user_profile = Profile.objects.get(user=request.user)
    return render(request,'privacy.html',{'user_profile':user_profile})

@login_required(login_url='login_url')
def userposts(request,pk):
    user_profile = Profile.objects.get(user=request.user)
    user_object = User.objects.get(username=pk)
    other_user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    for post in user_posts:
        post.is_liked_by_user = LikePost.objects.filter(post_id=post.id, username=request.user.username).exists()
        post.like_count = LikePost.objects.filter(post_id=post.id).count()
        post.comment_count = Comment.objects.filter(post=post).count()
    
    return render(request,'userposts.html',{'user_profile':user_profile,'user_posts':user_posts,'other_user_profile':other_user_profile})

@login_required(login_url='login_url')
def deletepost(request,pk):
    user_profile = Profile.objects.get(user=request.user)
    delete_post = Post.objects.get(id=pk)
    delete_post.delete()
    return redirect('userposts_url', pk=user_profile)

@login_required(login_url='login_url')
def load_comments(request):
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-created_at')

    comment_data = []
    for comment in comments:
        comment_data.append({
            "username": comment.user.username,
            "content": comment.content,
            "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return JsonResponse({"comments": comment_data})

@login_required(login_url='login_url')
def submit_comment(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        content = request.POST.get('content')

        post = Post.objects.get(id=post_id)
        comment = Comment.objects.create(post=post, user=request.user, content=content)

        comment_data = {
            "username": comment.user.username,
            "content": comment.content,
            "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }

        return JsonResponse({"comment": comment_data})

@login_required(login_url='login_url')
def delete_account(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        reason = request.POST["reason"]
        if reason:
            deleted_user = DeletedUsers.objects.create(username = request.user.username, reason = reason )
            deleted_user.save()
            delete_post = Post.objects.filter(user=str(request.user))
            delete_follower = FollowersCount.objects.filter(follower=user_profile)
            delete_following = FollowersCount.objects.filter(user=user_profile)
            delete_likes = LikePost.objects.filter(username=user_profile)
            delete_mycomments = Comment.objects.filter(user=user_profile.id_user)
            delete_user = User.objects.get(username = request.user)
            for post in delete_post:
                delete_comment = Comment.objects.filter(post_id=post.id)
                delete_like = LikePost.objects.filter(post_id = post.id)
                delete_comment.delete()
                delete_like.delete()
            delete_mycomments.delete()
            delete_likes.delete()
            delete_following.delete()
            delete_follower.delete()
            delete_post.delete()
            user_profile.delete()
            delete_user.delete()
            return redirect('login_url')
        else:
            messages.error(request,"We want your reason, Enter reason then delete")
            return redirect('delete_account')
            
    return render(request, 'delete account.html',{'user_profile':user_profile})