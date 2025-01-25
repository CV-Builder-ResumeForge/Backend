from django.db import models
from accounts.models import User
import uuid

# Personal Details
class PersonalDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="personal_details")
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=255, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} - {self.user.username}"

# Education
class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    personal_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE, related_name="educations")
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    grade = models.CharField(max_length=10, blank=True, null=True)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['personal_details', 'institution', 'degree'],
    #             name='unique_education_per_user'
    #         )
    #     ]

    def __str__(self):
        return f"{self.degree} at {self.institution}"

# Experience Model
class Experience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    personal_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE, related_name="experiences")
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)  # e.g., "Jan 2020 - Dec 2022"
    description = models.TextField(blank=True, null=True)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['personal_details', 'company', 'position', 'duration'],
    #             name='unique_experience_per_user'
    #         )
    #     ]

    def __str__(self):
        return f"{self.position} at {self.company}"


# Skill Model
class Skill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    personal_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE, related_name="skills")
    skill_name = models.CharField(max_length=100)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['personal_details', 'skill_name'],
    #             name='unique_skill_per_user'
    #         )
    #     ]

    def __str__(self):
        return self.skill_name


# Training Model
class Training(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    personal_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE, related_name="trainings")
    training_name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['personal_details', 'training_name', 'organization'],
    #             name='unique_training_per_user'
    #         )
    #     ]

    def __str__(self):
        return f"{self.training_name} at {self.organization}"


# Achievement Model
class Achievement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    personal_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE, related_name="achievements")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['personal_details', 'title', 'date'],
    #             name='unique_achievement_per_user'
    #         )
    #     ]

    def __str__(self):
        return self.title


# Project Model
class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    personal_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE, related_name="projects")
    project_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)  # For external project links
    duration = models.CharField(max_length=255, blank=True, null=True)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['personal_details', 'project_name'],
    #             name='unique_project_per_user'
    #         )
    #     ]

    def __str__(self):
        return self.project_name


# Language Model
class Language(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    personal_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE, related_name="languages")
    language_name = models.CharField(max_length=100)
    proficiency = models.CharField(
        max_length=50,
        choices=[
            ("Basic", "Basic"),
            ("Intermediate", "Intermediate"),
            ("Advanced", "Advanced"),
            ("Native", "Native"),
        ],
        default="Basic",
    )

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['personal_details', 'language_name', 'proficiency'],
    #             name='unique_language_per_user'
    #         )
    #     ]

    def __str__(self):
        return f"{self.language_name} ({self.proficiency})"


# Reference Model
class Reference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    personal_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE, related_name="references")
    name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=255)  # e.g., "Manager", "Colleague"
    contact = models.CharField(max_length=255)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['personal_details', 'name', 'relationship'],
    #             name='unique_reference_per_user'
    #         )
    #     ]

    def __str__(self):
        return f"{self.name} ({self.relationship})"
