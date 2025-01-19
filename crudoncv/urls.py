from django.urls import path
from .views import (
    PersonalDetailsAPIView, EducationAPIView, ExperienceAPIView, SkillAPIView, TrainingAPIView, AchievementAPIView,
    ProjectAPIView, LanguageAPIView, ReferenceAPIView
)

urlpatterns = [
    path('personal-details/', PersonalDetailsAPIView.as_view(), name='save-personal-details'),
    path('personal-details/<uuid:pk>/', PersonalDetailsAPIView.as_view()),  # Use <uuid:pk> for UUIDs
    path('educations/', EducationAPIView.as_view()),
    path('educations/<uuid:pk>/', EducationAPIView.as_view()),
    path('experiences/', ExperienceAPIView.as_view()),
    path('experiences/<uuid:pk>/', ExperienceAPIView.as_view()),
    path('skills/', SkillAPIView.as_view()),
    path('skills/<uuid:pk>/', SkillAPIView.as_view()),
    path('trainings/', TrainingAPIView.as_view()),
    path('trainings/<uuid:pk>/', TrainingAPIView.as_view()),
    path('achievements/', AchievementAPIView.as_view()),
    path('achievements/<uuid:pk>/', AchievementAPIView.as_view()),
    path('projects/', ProjectAPIView.as_view()),
    path('projects/<uuid:pk>/', ProjectAPIView.as_view()),
    path('languages/', LanguageAPIView.as_view()),
    path('languages/<uuid:pk>/', LanguageAPIView.as_view()),
    path('references/', ReferenceAPIView.as_view()),
    path('references/<uuid:pk>/', ReferenceAPIView.as_view()),
]
