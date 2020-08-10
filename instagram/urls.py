from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.home, name = 'home'),
    url(r'^signup/$', views.signup, name = 'signup'),
    url(r'^search/', views.search_results, name = 'search_results'),
    url(r'^user/(?P<username>\w+)', views.profile, name='profile'),
    url(r'^accounts/edit/', views.edit_profile, name='edit_profile'),
    url(r'^upload/$', views.upload_image, name='upload_image'),
    url(r'^follow/(?P<user_id>\d+)', views.follow, name = 'follow'),
    url(r'^unfollow/(?P<user_id>\d+)', views.unfollow, name='unfollow'),
    url(r'^comment/(?P<image_id>\d+)', views.comment, name='comment'),
    url(r'^like/(?P<image_id>\d+)', views.like, name='like'),
    url(r'^is_liked/', views.is_liked, name = 'is_liked')
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)