from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from profiler.serializers.posts_serializer import *
from profiler.models import *
from itertools import chain

class PostsView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format='json'):
        user = request.user
        try:
            profile = Profile.objects.get(user = user)
            friends = profile.friends.all()
            search = [profile.id]
            for friend in friends:
                search.append(friend.id)
            posts = Posts.objects.filter(profile__id__in=search).order_by('-date')
        except Exception:
            errors = {
                'noposts' : 'error'
            }
            return Response(errors,status=status.HTTP_400_BAD_REQUEST)
        serializer =PostsSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format='json'):
        user = request.user
        profile = Profile.objects.get(user=user)
        post = request.data.copy()
        tags = post.pop('tags', None)
        serializer = PostsSerializer(data=post)
        if serializer.is_valid():
            serializer.save(tags = tags, profile=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    def get(self, request, id,format='json'):
        try:
            posts = Posts.objects.get(id = id)
        except Exception:
            errors = {
                'noposts': 'error'
            }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = PostsDetailsSerializer(posts)
        return Response(serializer.data)

class DeletePost(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request, id):
        profile = Profile.objects.get(user = request.user)
        try:
            post = Posts.objects.get(id = id, profile=profile)
        except Posts.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GetPosts(APIView):
    def get(self, request, handel):
        profile = Profile.objects.get(handel = handel)
        posts = Posts.objects.filter(profile=profile)
        if len(posts) == 0:
            errors = {
                'noposts': 'No posts have been created'
            }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = PostsSerializer(posts, many=True)
        return Response(serializer.data)


class CommentView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request,id, format='json'):
        user = request.user
        profile = Profile.objects.get(user=user)
        post = request.data
        posts = Posts.objects.get(id=id)
        serializer = CommentSerializer(data=post)
        if serializer.is_valid():
            serializer.save(post = posts, profile=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddLike(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, id):
        profile = Profile.objects.get(user=request.user)
        try:
            post = Posts.objects.get(id=id)
        except Profile.DoesNotExist:
            errors = {
                'error' : 'there is no post with the id'
            }
            return Response(errors,status=status.HTTP_400_BAD_REQUEST)
        post.likes.add(profile)
        post.save()
        return Response(status=status.HTTP_201_CREATED)