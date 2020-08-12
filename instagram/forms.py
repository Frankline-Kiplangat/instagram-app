from django import forms
from .models import Profile,Image,Comment


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude=['user']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude =['likes','profile']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['picture', 'comment_title']


class MessageForm(forms.Form):
    subject = forms.CharField(max_length=100)
    To = forms.CharField(max_length=100)
