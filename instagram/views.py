from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Comments, Image, Profile, Likes
from .forms import SignUpForm, ImageForm, CommentForm, ProfileForm
# from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from friendship.models import Friend, Follow, Block
from friendship.exceptions import AlreadyExistsError
# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate Your Instagram Account'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required(login_url='/accounts/register/')
def timeline(request):
    images = Image.get_all_images()
    likes = Likes.objects.all()
    profiles = Profile.objects.all()
    comments = Comments.objects.all()
    profile_pic = User.objects.all()
    following = Follow.objects.following(request.user)
    form = CommentForm()
    id = request.user.id
    liked_images = Likes.objects.filter(user_id=id)
    mylist = [i.image_id for i in liked_images]
    title = 'Home'
    return render(request, 'index.html', {'title':title, 'images':images, 'profile_pic':profile_pic, 'following': following, 'form':form, 'comments':comments, 'profiles':profiles, 'likes':likes, 'list':mylist})

@login_required(login_url='/accounts/login/')
def comment(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(Image, pk = image_id)
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.image = image
            comment.save()
            return redirect('index')
    else:
        form = CommentForm()

    title = 'Home'
    return render(request, 'index.html', {'title':title})


@login_required(login_url='/accounts/login/')
def profile(request, username):
    title = 'Profile'
    profile = User.objects.get(username=username)
    comments = Comments.objects.all()
    users = User.objects.get(username=username)
    follow = len(Follow.objects.followers(users))
    following = len(Follow.objects.following(users))
    people_following = Follow.objects.following(request.user)
    id = request.user.id
    liked_images = Likes.objects.filter(user_id=id)
    mylist = [i.image_id for i in liked_images]
    form = CommentForm()

    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)

    images = Image.get_profile_pic(profile.id)
    return render(request, 'profile.html', {'title':title, 'comments':comments, 'profile':profile, 'profile_details':profile_details, 'images':images, 'follow':follow, 'following':following, 'list':mylist, 'people_following':people_following, 'form':form})


