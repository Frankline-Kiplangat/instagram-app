from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from pyuploadcare.dj.models import ImageField
from friendship.models import Friend,Follow,Block

# Create your models here.

class Profile(models.Model):
    profile_pic = models.ImageField()
    bio = models.CharField(max_length=100,blank=True)
    user = models.ForeignKey(User,blank=True, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return self.bio

    #Save profile
    def profile_save(self):
        self.save()

     #delete profile
    def delete_profile(self):
        self.delete()

     #Get profile
    @classmethod
    def get_by_id(cls, id):
        profile = Profile.objects.filter(user=id)
        return profile

    @classmethod
    def get_profile_by_username(cls, owner):
        profiles = cls.objects.filter(user__contains=user)
        return profiles


 #Image
class Image(models.Model):
    time_created= models.DateTimeField(default=datetime.now, blank=True)
    my_image=ImageField(manual_crop='1080x800', blank=True)
    message = models.CharField(max_length=80, default='Hey', blank=True)
    name = models.CharField(max_length=80)
    caption = models.TextField(blank=True)
    profile = models.ForeignKey(User, blank=True,on_delete=models.CASCADE)
    profile_details = models.ForeignKey(Profile)


    def __str__(self):
        return self.name

    #Save image
    def save_image(self):
        self.save()

    #Delete image
    def delete_image(self):
        self.delete()

    #Get image
    @classmethod
    def get_profile_images(cls, profile):
        images = Image.objects.filter(profile__pk=profile)
        return images

# Likes
class Likes(models.Model):
    likes = models.ForeignKey(User)
    image = models.ForeignKey(Image)


class Comment(models.Model):
    image = models.ForeignKey(Image,blank=True, on_delete=models.CASCADE,related_name='comment')
    comment_title = models.ForeignKey(User, blank=True)
    comment= models.TextField()

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()

    @classmethod
    def get_image_comments(cls, id):
        comments = Comment.objects.filter(image__pk=id)
        return comments

    def __str__(self):
        return str(self.comment)






