import datetime
from django.db import models
from django.contrib.auth.models import User


class Skills(models.Model):
    lang = models.CharField(max_length=128)

    def __str__(self):
        return self.lang

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    handel = models.CharField(max_length=128)
    fullname = models.CharField(max_length = 512)
    avatar = models.ImageField(upload_to='avatars/' ,null=True, blank=True)
    location = models.CharField(max_length=128)
    website = models.URLField(max_length=256,null= True, blank = True)
    status = models.CharField(max_length=128)
    skills = models.ManyToManyField(Skills)
    bio = models.CharField(max_length=512)
    linkedIn = models.URLField(max_length = 512,null=True, blank = True)
    gitusername = models.CharField(max_length=128)
    friends = models.ManyToManyField("Profile")

class Education(models.Model):
    degree = models.CharField(max_length=128)
    school = models.CharField(max_length=128)
    location = models.CharField(max_length=256)
    fieldOfStudy = models.CharField(max_length=128)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=512)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.school

class Experience(models.Model):
    title = models.CharField(max_length=128)
    company = models.CharField(max_length=128)
    location = models.CharField(max_length=256)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)
    current = models.BooleanField(default=False)
    description = models.CharField(max_length=512)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.company


class Tags(models.Model):
    tag = models.CharField(max_length=128)

    def __str__(self):
        return self.tag

class Posts(models.Model):
    title = models.CharField(max_length=512)
    date = models.DateTimeField(auto_now_add=True)
    hasimg = models.BooleanField(default=False)
    img = models.ImageField(upload_to='posts/' ,null=True, blank=True)
    description = models.CharField(max_length=2048)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    likes = models.ManyToManyField(Profile,related_name='%(class)s_likes')
    tags = models.ManyToManyField(Tags)

class Comments(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.CharField(max_length=1024)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)