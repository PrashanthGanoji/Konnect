from django.urls import path
from django.conf.urls import include, url
from django.views.generic import TemplateView

from profiler.serializers.jwt_user_serializer import CustomJWTSerializer
from profiler.views import *
from profiler.apiViews.userApiView import *
from profiler.apiViews.profileApiView import *
from profiler.apiViews.postsApiView import *
from rest_framework_jwt.views import ObtainJSONWebToken


urlpatterns = [
    path('users',UserList.as_view(), name = "list_users"), #create User, list users , **public
    path('profile', ProfileView.as_view(),name="view_profile"), #create profile(can even pass edu & exp), get current users profile, **private

    path('profile/all', ProfileList.as_view(), name="list_profiles"), #list all users, **public
    path('profile/handel/<str:handel>', ProfileByHandel.as_view(), name="view_profile_handel"), #profile detail view using handel, **public
    path('user/<int:id>', ProfileById.as_view(), name="view_profile_id"), #profile detail view using userid, **public

    path('profile/exp', ExperienceView.as_view(), name="profile_exp"), #view exp, add exp
    path('profile/edu', EducationView.as_view(), name="profile_edu"), #view edu, add edu

    path('profile/exp/<int:id>', DeleteExperienceView.as_view(), name="del_profile_exp"), #delete exp
    path('profile/edu/<int:id>', DeleteEducationView.as_view(), name="del_profile_edu"),  #delete edu

    path('profile/friends/<int:id>', AddFriend.as_view()), #add friend
    path('profile/getfriends/<int:id>', GetFriends.as_view()),

    path('profile/posts', PostsView.as_view()), #get posts of friends and post a new post
    path('profile/posts/<int:id>', PostDetailView.as_view()), #get detail info of a post
    path('profile/posts/<int:id>/comments', CommentView.as_view()), #post comment
    path('profile/<str:handel>/posts', GetPosts.as_view()), #get posts of a user with handel
    path('profile/delete_post/<int:id>', DeletePost.as_view()), #delete posts of currently logged user
    path('profile/post/like/<int:id>', AddLike.as_view()), #like a post with given id

    path('login', ObtainJSONWebToken.as_view(serializer_class=CustomJWTSerializer)), #jwt route using custom serilizer

    url(r'^(?P<path>.*)/$', TemplateView.as_view(template_name="index.html")),
]