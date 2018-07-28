from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from profiler.serializers.profile_serializer import *
from profiler.models import *


class ProfileView(APIView):
    """
    Creates the user.
    """
    permission_classes = (IsAuthenticated,)
    def get(self, request, format='json'):
        user = request.user
        try:
            profile = Profile.objects.get(user = user)
        except Profile.DoesNotExist:
            errors = {
                'noprofile' : 'there is no profile for this user'
            }
            return Response(errors,status=status.HTTP_400_BAD_REQUEST)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request, format='json'):
        user = request.user
        post = request.data.copy()
        skills = post.pop('skills')
        serializer = ProfileSerializer(data=post)
        if serializer.is_valid():
            serializer.save(user = user, skills = skills)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format="json"):
        try:
            profile = Profile.objects.get(user = request.user)
        except Profile.DoesNotExist:
            errors = {
                'noprofile' : 'there is no profile for this user'
            }
            return Response(errors,status=status.HTTP_400_BAD_REQUEST)
        post = request.data.copy()
        print('in post',post)
        skills = post.pop('skills')
        serializer = ProfileSerializer(data=post, instance=profile)
        if serializer.is_valid():
            serializer.save(skills = skills)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            errors = {
                'noprofile' : 'there is no profile for this user'
            }
            return Response(errors,status=status.HTTP_400_BAD_REQUEST)

        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileList(APIView):
    def get(self, request, format='json'):
        profiles = self.get_queryset()
        if len(profiles) == 0:
            errors = {
                'emptyProfileList': 'No profiles have been created'
            }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Profile.objects.all()
        username = self.request.query_params.get('name', None)
        skillset = self.request.query_params.get('skills',None)
        location = self.request.query_params.get('location',None)

        if username is not None:
            queryset = queryset.filter(fullname__icontains=username)
        if skillset is not None:
            queryset = queryset.filter(skills__lang__iexact = skillset)
        if location is not None:
            queryset = queryset.filter(location__icontains = location)
        return queryset

class ProfileById(APIView):
    def get(self, request, id, format='json'):
        try:
            profile = Profile.objects.get(pk = id)
        except Profile.DoesNotExist:
            errors = {
                'noprofile': 'No profiles with that id'
            }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

class ProfileByHandel(APIView):
    def get(self, request, handel, format='json'):
        try:
            profile = Profile.objects.get(handel = handel)
        except Profile.DoesNotExist:
            errors = {
                'noprofile': 'No profiles with that id'
            }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class ExperienceView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request, format='json'):
        profile = Profile.objects.get(user = request.user)
        experiences = Experience.objects.filter(profile = profile)
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data)

    def post(self,request,format='json'):
        profile = Profile.objects.get(user=request.user)
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile = profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteExperienceView(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request, id, format='json'):
        experience = Experience.objects.get(pk = id)
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EducationView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format='json'):
        profile = Profile.objects.get(user=request.user)
        education = Education.objects.filter(profile=profile)
        serializer = EducationSerializer(education, many=True)
        return Response(serializer.data)

    def post(self,request,format='json'):
        profile = Profile.objects.get(user=request.user)
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile = profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteEducationView(APIView):
    permission_classes = (IsAuthenticated,)
    def delete(self, request, id, format='json'):
        edu = Education.objects.get(pk = id)
        edu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddFriend(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, id):
        profile = Profile.objects.get(user=request.user)
        try:
            f = Profile.objects.get(id=id)
        except Profile.DoesNotExist:
            errors = {
                'error' : 'there is no profile with the id'
            }
            return Response(errors,status=status.HTTP_400_BAD_REQUEST)
        profile.friends.add(f)
        profile.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        profile = Profile.objects.get(user=request.user)
        unfriend = Profile.objects.get(id = id)
        profile.friends.remove(unfriend)
        return Response(status=status.HTTP_204_NO_CONTENT)

class GetFriends(APIView):
    def get(self, request, id):
        profile = Profile.objects.get(id = id)
        friends = profile.friends.all()
        if len(friends) == 0:
            errors = {
                'emptyProfileList': 'No profiles have been created'
            }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProfileSerializer(friends, many=True)
        return Response(serializer.data)
