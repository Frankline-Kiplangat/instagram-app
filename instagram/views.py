from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from friendship.exceptions import AlreadyExistsError
from .models import Image, Profile,Comment,Follow,Likes
from .forms import MessageForm, ProfileForm, ImageForm, CommentForm

# Create your views here.

@login_required(login_url='/accounts/login/')
def home(request):
    current_user = request.user
    all_images = Image.objects.all()
    comments = Comment.objects.all()
    likes = Likes.objects.all
    profile = Profile.objects.all()
    return render(request,'index.html',locals())

# Explore
@login_required(login_url='/login')
def explore(request):
    images = Image.objects.all()
    all_profiles = Profile.objects.all()
    return render(request, 'main/explore.html',{'images': images,'all_profiles' : all_profiles })

# Message
@login_required(login_url='/accounts/login/')
def messages(request):
    images = Image.objects.all()
    messageform = MessageForm()
    return render(request, 'main/messages.html',{'images': images, 'messageform':messageform})

# Search
def search(request):
    profiles = User.objects.all()
    if 'username' in request.GET and request.GET['username']:
        search_term = request.GET.get('username')
        results = User.objects.filter(username__icontains=search_term)
        return render(request,'search.html',locals())
    return redirect(home)

# Add image
@login_required(login_url='accounts/login/')
def add_image(request):
    current_user = request.user
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            add=form.save(commit=False)
            add.profile = current_user
            add.save()
            return redirect('home')
    else:
        form = ImageForm()
    return render(request,'image.html',locals())

# profile
@login_required(login_url='/login')
def profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            profile =form.save(commit=False)
            profile.user = current_user
            profile.save()
    else:
        form=ProfileForm()

    return render(request, 'profile/new_user.html', locals())

# all profiles displayed
@login_required(login_url='/accounts/login/')
def display_profile(request, id):
    seekuser=User.objects.filter(id=id).first()
    profile = seekuser.profile
    profile_details = Profile.get_by_id(id)
    images = Image.get_profile_images(id)

    users = User.objects.get(id=id)
    follower = len(Follow.objects.followers(users))
    following = len(Follow.objects.following(users))
    people=User.objects.all()
    pip_following=Follow.objects.following(request.user)

    return render(request,'profile/profile.html',locals())

# Comment
def comment(request,image_id):
    current_user=request.user
    image = Image.objects.get(id=image_id)
    profile_owner = User.objects.get(username=current_user)
    comments = Comment.objects.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = image
            comment.comment_title = current_user
            comment.save()
        return redirect(home)

    else:
        form = CommentForm()

    return render(request, 'comment.html', locals())


def follow(request,user_id):
    users=User.objects.get(id=user_id)
    follow = Follow.objects.add_follower(request.user, users)

    return redirect('/profile/', locals())


def like(request, image_id):
    current_user = request.user
    image=Image.objects.get(id=image_id)
    new_like,created= Likes.objects.get_or_create(likes=current_user, image=image)
    new_like.save()

    return redirect('home')