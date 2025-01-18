from rest_framework import serializers
from .models import (
    PersonalDetails, Education, Experience, Skill,
    Training, Achievement, Project, Language, Reference
)

# Personal Details Serializer
class PersonalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDetails
        fields = '__all__'

# Education Serializer
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

# Experience Serializer
class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

# Skill Serializer
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

# Training Serializer
class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = '__all__'

# Achievement Serializer
class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'

# Project Serializer
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

# Language Serializer
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

# Reference Serializer
class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = '__all__'
