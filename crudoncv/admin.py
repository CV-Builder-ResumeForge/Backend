from django.contrib import admin
from .models import (
    PersonalDetails, Education, Experience, Skill,
    Training, Achievement, Project, Language, Reference
)

# Personal Details Admin
class PersonalDetailsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'location', 'user')
    search_fields = ('full_name', 'email', 'user__username')

admin.site.register(PersonalDetails, PersonalDetailsAdmin)

# Education Admin
class EducationAdmin(admin.ModelAdmin):
    list_display = ('institution', 'degree', 'year', 'grade', 'personal_details')
    search_fields = ('institution', 'degree', 'personal_details__full_name')

admin.site.register(Education, EducationAdmin)

# Experience Admin
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('company', 'position', 'duration', 'personal_details')
    search_fields = ('company', 'position', 'personal_details__full_name')

admin.site.register(Experience, ExperienceAdmin)

# Skill Admin
class SkillAdmin(admin.ModelAdmin):
    list_display = ('skill_name', 'personal_details')
    search_fields = ('skill_name', 'personal_details__full_name')

admin.site.register(Skill, SkillAdmin)

# Training Admin
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('training_name', 'organization', 'date', 'personal_details')
    search_fields = ('training_name', 'organization', 'personal_details__full_name')

admin.site.register(Training, TrainingAdmin)

# Achievement Admin
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'personal_details')
    search_fields = ('title', 'personal_details__full_name')

admin.site.register(Achievement, AchievementAdmin)

# Project Admin
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'description', 'personal_details')
    search_fields = ('project_name', 'personal_details__full_name')

admin.site.register(Project, ProjectAdmin)

# Language Admin
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('language_name', 'proficiency', 'personal_details')
    search_fields = ('language_name', 'personal_details__full_name')

admin.site.register(Language, LanguageAdmin)

# Reference Admin
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'relationship', 'contact', 'personal_details')
    search_fields = ('name', 'personal_details__full_name')

admin.site.register(Reference, ReferenceAdmin)
