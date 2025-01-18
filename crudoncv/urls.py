from django.urls import path
from .views import (
    PersonalDetailsAPIView, EducationAPIView, ExperienceAPIView, SkillAPIView, TrainingAPIView, AchievementAPIView,
    ProjectAPIView, LanguageAPIView, ReferenceAPIView
    # Add other views as needed
)

urlpatterns = [
    path('personal-details/', PersonalDetailsAPIView.as_view()),
    path('personal-details/<int:pk>/', PersonalDetailsAPIView.as_view()),
    path('educations/', EducationAPIView.as_view()),
    path('educations/<int:pk>/', EducationAPIView.as_view()),
    path('experiences/', ExperienceAPIView.as_view()),
    path('experiences/<int:pk>/', ExperienceAPIView.as_view()),
    path('skills/', SkillAPIView.as_view()),
    path('skills/<int:pk>/', SkillAPIView.as_view()),
    path('trainings/', TrainingAPIView.as_view()),
    path('trainings/<int:pk>/', TrainingAPIView.as_view()),
    path('achievements/', AchievementAPIView.as_view()),
    path('achievements/<int:pk>/', AchievementAPIView.as_view()),
    path('projects/', ProjectAPIView.as_view()),
    path('projects/<int:pk>/', ProjectAPIView.as_view()),
    path('languages/', LanguageAPIView.as_view()),
    path('languages/<int:pk>/', LanguageAPIView.as_view()),
    path('references/', ReferenceAPIView.as_view()),
    path('references/<int:pk>/', ReferenceAPIView.as_view()),
]
