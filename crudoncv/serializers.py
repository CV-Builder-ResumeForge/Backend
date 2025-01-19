from rest_framework import serializers
from .models import (
    PersonalDetails, Education, Experience, Skill,
    Training, Achievement, Project, Language, Reference
)

from accounts.models import User

# Personal Details Serializer
class PersonalDetailsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PersonalDetails
        fields = '__all__'

# Education Serializer
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

    def validate(self, data):
        # Check if a record already exists for the given personal_details, institution, and degree
        if Education.objects.filter(
            personal_details=data['personal_details'],
            institution=data['institution'],
            degree=data['degree']
        ).exists():
            raise serializers.ValidationError("This education record already exists.")
        return data


# Experience Serializer
class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

    def validate(self, data):
        if Experience.objects.filter(
            personal_details=data['personal_details'],
            company=data['company'],
            position=data['position'],
            duration=data['duration']
        ).exists():
            raise serializers.ValidationError("This experience record already exists.")
        return data

# Skill Serializer
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

    def validate(self, data):
        if Skill.objects.filter(
            personal_details=data['personal_details'],
            skill_name=data['skill_name']
        ).exists():
            raise serializers.ValidationError("This skill already exists.")
        return data

# Training Serializer
class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = '__all__'

    def validate(self, data):
        if Training.objects.filter(
            personal_details=data['personal_details'],
            training_name=data['training_name'],
            organization=data['organization']
        ).exists():
            raise serializers.ValidationError("This training record already exists.")
        return data


# Achievement Serializer
class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = '__all__'

    def validate(self, data):
        if Achievement.objects.filter(
            personal_details=data['personal_details'],
            title=data['title'],
            date=data['date']
        ).exists():
            raise serializers.ValidationError("This achievement already exists.")
        return data

# Project Serializer
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def validate(self, data):
        if Project.objects.filter(
            personal_details=data['personal_details'],
            project_name=data['project_name']
        ).exists():
            raise serializers.ValidationError("This project already exists.")
        return data

# Language Serializer
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

    def validate(self, data):
        if Language.objects.filter(
            personal_details=data['personal_details'],
            language_name=data['language_name'],
            proficiency=data['proficiency']
        ).exists():
            raise serializers.ValidationError("This language skill already exists.")
        return data

# Reference Serializer
class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = '__all__'

    def validate(self, data):
        if Reference.objects.filter(
            personal_details=data['personal_details'],
            name=data['name'],
            relationship=data['relationship']
        ).exists():
            raise serializers.ValidationError("This reference already exists.")
        return data
