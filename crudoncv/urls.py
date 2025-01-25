from django.urls import path
from .views import (
    PersonalDetailsAPIView, EducationAPIView, ExperienceAPIView, SkillAPIView, TrainingAPIView, AchievementAPIView,
    ProjectAPIView, LanguageAPIView, ReferenceAPIView
)

urlpatterns = [
    path('api/personal-details/', PersonalDetailsAPIView.as_view(), name='save-personal-details'),
    path('api/personal-details/<uuid:pk>/', PersonalDetailsAPIView.as_view()),  # Use <uuid:pk> for UUIDs
    path('api/educations/', EducationAPIView.as_view()),
    path('api/educations/<uuid:pk>/', EducationAPIView.as_view()),
    path('api/experiences/', ExperienceAPIView.as_view()),
    path('api/experiences/<uuid:pk>/', ExperienceAPIView.as_view()),
    path('api/skills/', SkillAPIView.as_view()),
    path('api/skills/<uuid:pk>/', SkillAPIView.as_view()),
    path('api/trainings/', TrainingAPIView.as_view()),
    path('api/trainings/<uuid:pk>/', TrainingAPIView.as_view()),
    path('api/achievements/', AchievementAPIView.as_view()),
    path('api/achievements/<uuid:pk>/', AchievementAPIView.as_view()),
    path('api/projects/', ProjectAPIView.as_view()),
    path('api/projects/<uuid:pk>/', ProjectAPIView.as_view()),
    path('api/languages/', LanguageAPIView.as_view()),
    path('api/languages/<uuid:pk>/', LanguageAPIView.as_view()),
    path('api/references/', ReferenceAPIView.as_view()),
    path('api/references/<uuid:pk>/', ReferenceAPIView.as_view()),
]
