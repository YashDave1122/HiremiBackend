from rest_framework import serializers
from .models import Job, Application, Skill, Interest, UserProfile

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'
        extra_kwargs = {
            'interest': {'validators': []}  
        }

class UserProfileSerializer(serializers.ModelSerializer):
    interests = InterestSerializer(many=True, read_only=True)
    interest_ids = serializers.PrimaryKeyRelatedField(
        queryset=Interest.objects.all(), source="interests", many=True, write_only=True
    )

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'interests', 'interest_ids']