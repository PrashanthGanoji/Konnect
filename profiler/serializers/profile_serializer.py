from rest_framework import serializers
from profiler.models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'first_name', 'last_name', 'email')

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ('id','degree', 'school', 'location', 'fieldOfStudy', 'start', 'end', 'description')
        extra_kwargs = {'end' :{'required':False}}

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        edu = Education(profile= profile, **validated_data)
        edu.save()
        return edu

    def update(self, instance, validated_data):
        pass

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ('id','title', 'company', 'location', 'start', 'end', 'current', 'description')
        extra_kwargs = {'end': {'required': False}}

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        exp = Experience(profile=profile, **validated_data)
        exp.save()
        return exp

    def update(self, instance, validated_data):
        pass

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ('lang')


class ProfileMini(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    handel = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )
    friends = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    skills = serializers.SlugRelatedField(many=True, slug_field='lang', read_only=True)
    class Meta:
        model = Profile
        fields = ('id','user','handel', 'fullname', 'avatar', 'location','skills','friends')


class ProfileSerializer(serializers.ModelSerializer):
    education_set = EducationSerializer(many=True, required=False)
    experience_set = ExperienceSerializer(many=True, required=False)
    user = UserSerializer(required=False)
    friends = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    skills = serializers.SlugRelatedField(many=True,slug_field='lang', read_only=True)
    handel = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )

    def create(self, validated_data):
        user = validated_data.pop('user')
        skillsData = validated_data.pop('skills')
        educationData = validated_data.pop('education_set', None)
        experienceData  = validated_data.pop('experience_set', None)
        profile = Profile(user = user, **validated_data)
        profile.save()
        if educationData:
            for item in educationData:
                education = Education(profile=profile, **item)
                education.save()
        if experienceData:
            for item in experienceData:
                experience = Experience(profile = profile, **item)
                experience.save()

        for lang in skillsData:
            skill, created = Skills.objects.get_or_create(lang=lang)
            profile.skills.add(skill)
        profile.save()
        return profile

    def update(self, instance, validated_data):
        instance.handel = validated_data.get('handel')
        instance.avatar = validated_data.get('avatar',instance.avatar)
        if validated_data.get('website', None):
            instance.website = validated_data.get('website')
        instance.location = validated_data.get('location')
        instance.fullname = validated_data.get('fullname')
        instance.linkedin = validated_data.get('linkedin', instance.linkedin)
        instance.status = validated_data.get('status')
        instance.bio = validated_data.get('bio')
        instance.gitusername = validated_data.get('gitusername')
        skillsData = validated_data.pop('skills')
        instance.skills.clear()
        for lang in skillsData:
            skill, created = Skills.objects.get_or_create(lang=lang)
            instance.skills.add(skill)
        instance.save()
        return instance

    class Meta:
        model = Profile
        fields = ('id','user','handel', 'fullname', 'avatar', 'location', 'website','status','skills','bio','gitusername', 'linkedIn','education_set', 'experience_set', 'friends')
        extra_kwargs = {'user': {'required': False}, 'education_set': {'required': False}, 'experience_set': {'required': False}, 'avatar':{'required':False},'linkedIn':{'required':False}, 'website':{'required':False}}

    def get_validation_exclusions(self):
        exclusions = super(ProfileSerializer, self).get_validation_exclusions()
        return exclusions + ['education_set', 'experience_set', 'user', 'friends']
