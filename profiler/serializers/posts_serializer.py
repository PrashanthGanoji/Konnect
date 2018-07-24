from rest_framework import serializers
from profiler.models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from profiler.serializers.profile_serializer import ProfileSerializer,ProfileMini


class CommentSerializer(serializers.ModelSerializer):
    user = ProfileMini(required=False)
    class Meta:
        model = Comments
        fields = ('id','date', 'user', 'description')
        extra_kwargs = {'date': {'required': False}, 'user': {'required': False}, 'id': {'required': False}}

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        post = validated_data.pop('post')
        cmt = Comments(post=post,user=profile, **validated_data)
        cmt.save()
        return cmt


class PostsSerializer(serializers.ModelSerializer):
    profile = ProfileMini(required=False)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tags = serializers.SlugRelatedField(many=True, slug_field='tag', read_only=True)

    class Meta:
        model = Posts
        fields = ('id','title', 'date', 'hasimg', 'img', 'description', 'profile', 'likes', 'tags')
        extra_kwargs = {'img' :{'required':False}, 'tags':{'required':False},'profile':{'required':False}, 'date':{'required':False}, 'likes':{'required':False}}

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        tags = validated_data.pop('tags')
        posts = Posts(profile=profile, **validated_data)
        posts.save()
        if tags:
            for tag in tags:
                tag, created = Tags.objects.get_or_create(tag=tag)
                posts.tags.add(tag)
        posts.save()
        return posts

class PostsDetailsSerializer(serializers.ModelSerializer):
    comments_set = CommentSerializer(many=True, required=False)
    profile = ProfileMini(required=False)
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tags = serializers.SlugRelatedField(many=True, slug_field='tag', read_only=True)

    class Meta:
        model = Posts
        fields = ('id','title', 'date', 'hasimg', 'img', 'description', 'profile', 'comments_set', 'likes', 'tags')