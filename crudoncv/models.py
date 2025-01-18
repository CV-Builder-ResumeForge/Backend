from django.db import models
from accounts.models import User

# Personal Details
class PersonalDetails(models.Model):
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
    personal_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE, related_name="educations")
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    grade = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.degree} at {self.institution}"

# Experience
class Experience(models.Model):
    personal_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE, related_name="experiences")
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)  # e.g., "Jan 2020 - Dec 2022"
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.position} at {self.company}"

# Skills
class Skill(models.Model):
    personal_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE, related_name="skills")
    skill_name = models.CharField(max_length=100)

    def __str__(self):
        return self.skill_name

# Trainings
class Training(models.Model):
    personal_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE, related_name="trainings")
    training_name = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.training_name} at {self.organization}"

# Achievements
class Achievement(models.Model):
    personal_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE, related_name="achievements")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

# Projects
class Project(models.Model):
    personal_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE, related_name="projects")
    project_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)  # For external project links
    duration = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.project_name

# Languages
class Language(models.Model):
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

    def __str__(self):
        return f"{self.language_name} ({self.proficiency})"

# References
class Reference(models.Model):
    personal_details = models.ForeignKey(PersonalDetails, on_delete=models.CASCADE, related_name="references")
    name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=255)  # e.g., "Manager", "Colleague"
    contact = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.relationship})"
