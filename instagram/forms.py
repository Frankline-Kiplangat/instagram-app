from django import forms 
from .models import Comments, Image, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(forms.Form):
    email = forms.EmailField(max_length=50, help_text="Required")
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['likes', 'posted', 'profile', 'profile_det', 'comments']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ['image', 'user']