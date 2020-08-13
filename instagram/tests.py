from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Image, Profile,Comment

# Create your tests here.

class ProfileTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = User.objects.create_user('Happy', 'secret')
        cls.profile1 = Profile(profile_pic='https://unsplash.it/1200/768.jpg?image=76',
                                            bio='Live life',
                                            user=cls.user)

 # Testing  instance
    def test_instance(cls):
        cls.assertTrue(isinstance(cls.profile1, Profile))

   # Testing Save Method
    def save_method_test(self):
        self.profile1.save_profile()
        images = Image.objects.all()
        self.assertTrue(len(images) > 0)



# Image testing

class ImageTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = User.objects.create_user('Happy', 'secret')
        cls.new_profile = Profile(profile_pic='/static/images/IMG_2046.png',bio='Live life', user=cls.user)
        cls.new_image = Image(my_image='/static/images/IMG_2046.png', caption='Travel', profile=cls.new_profile)

    def test_instance_true(cls):
        cls.assertTrue(isinstance(cls.new_image, Image))

    def test_save_image_method(self):
        self.new_image.save_image()
        images = Image.objects.all()
        self.assertTrue(len(images) == 1)

    def tearDown(self):
        Image.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()

# Comment
class CommentTestClass(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.new_user = User.objects.create_user('Happy', 'secret')

        cls.new_profile = Profile(profile_pic='/static/images/IMG_2046.png',bio='Like it',user=cls.new_user)
        self.new_profile.save()

        cls.new_image = Image(my_image='/static/images/IMG_2046.png',
                               caption='Travel', profile='',profile_details=cls.new_user)
        self.new_image.save()

        cls.new_comment = Comment(
            image=self.new_image, comment_title=self.new_profile, comment='Like it')

    def test_instance_true(cls):
        cls.new_comment.save()
        cls.assertTrue(isinstance(cls.new_comment, Comment))

    def test_save_comment(self):
        self.new_comment.save_comment()
        comments = Comment.objects.all()
        self.assertTrue(len(comments) == 1)

    def tearDown(self):
        Image.objects.all().delete()
        Profile.objects.all().delete()
        User.objects.all().delete()
        Comment.objects.all().delete()