from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import (
    PersonalDetails, Education, Experience, Skill,
    Training, Achievement, Project, Language, Reference
)
from .serializers import (
    PersonalDetailsSerializer, EducationSerializer, ExperienceSerializer,
    SkillSerializer, TrainingSerializer, AchievementSerializer,
    ProjectSerializer, LanguageSerializer, ReferenceSerializer
)

# Personal Details API View
class PersonalDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        personal_details = PersonalDetails.objects.filter(user=request.user)
        serializer = PersonalDetailsSerializer(personal_details, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PersonalDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            personal_detail = PersonalDetails.objects.get(pk=pk, user=request.user)
        except PersonalDetails.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PersonalDetailsSerializer(personal_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            personal_detail = PersonalDetails.objects.get(pk=pk, user=request.user)
            personal_detail.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PersonalDetails.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


# Education API View
class EducationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        education = Education.objects.filter(personal_details__user=request.user)
        serializer = EducationSerializer(education, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            education = Education.objects.get(pk=pk, personal_details__user=request.user)
        except Education.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EducationSerializer(education, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            education = Education.objects.get(pk=pk, personal_details__user=request.user)
            education.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Education.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


# Repeat the above structure for Experience, Skills, etc.

class ExperienceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        experience = Experience.objects.filter(personal_details__user=request.user)
        serializer = ExperienceSerializer(experience, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            experience = Experience.objects.get(pk=pk, personal_details__user=request.user)
        except Experience.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExperienceSerializer(experience, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            experience = Experience.objects.get(pk=pk, personal_details__user=request.user)
            experience.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Experience.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


# Skill API View
class SkillAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        skills = Skill.objects.filter(personal_details__user=request.user)
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            skill = Skill.objects.get(pk=pk, personal_details__user=request.user)
        except Skill.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SkillSerializer(skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            skill = Skill.objects.get(pk=pk, personal_details__user=request.user)
            skill.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Skill.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


# Training API View
class TrainingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trainings = Training.objects.filter(personal_details__user=request.user)
        serializer = TrainingSerializer(trainings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TrainingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            training = Training.objects.get(pk=pk, personal_details__user=request.user)
        except Training.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TrainingSerializer(training, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            training = Training.objects.get(pk=pk, personal_details__user=request.user)
            training.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Training.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


# Achievement API View
class AchievementAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        achievements = Achievement.objects.filter(personal_details__user=request.user)
        serializer = AchievementSerializer(achievements, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AchievementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            achievement = Achievement.objects.get(pk=pk, personal_details__user=request.user)
        except Achievement.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AchievementSerializer(achievement, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            achievement = Achievement.objects.get(pk=pk, personal_details__user=request.user)
            achievement.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Achievement.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


# Project API View
class ProjectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.filter(personal_details__user=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            project = Project.objects.get(pk=pk, personal_details__user=request.user)
        except Project.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            project = Project.objects.get(pk=pk, personal_details__user=request.user)
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


# Language API View
class LanguageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        languages = Language.objects.filter(personal_details__user=request.user)
        serializer = LanguageSerializer(languages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LanguageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            language = Language.objects.get(pk=pk, personal_details__user=request.user)
        except Language.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = LanguageSerializer(language, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            language = Language.objects.get(pk=pk, personal_details__user=request.user)
            language.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Language.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


# Reference API View
class ReferenceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        references = Reference.objects.filter(personal_details__user=request.user)
        serializer = ReferenceSerializer(references, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReferenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            reference = Reference.objects.get(pk=pk, personal_details__user=request.user)
        except Reference.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReferenceSerializer(reference, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            reference = Reference.objects.get(pk=pk, personal_details__user=request.user)
            reference.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Reference.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)