# Generated by Django 5.1.4 on 2025-02-19 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crudoncv', '0002_achievement_unique_achievement_per_user_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='achievement',
            name='unique_achievement_per_user',
        ),
        migrations.RemoveConstraint(
            model_name='education',
            name='unique_education_per_user',
        ),
        migrations.RemoveConstraint(
            model_name='experience',
            name='unique_experience_per_user',
        ),
        migrations.RemoveConstraint(
            model_name='language',
            name='unique_language_per_user',
        ),
        migrations.RemoveConstraint(
            model_name='project',
            name='unique_project_per_user',
        ),
        migrations.RemoveConstraint(
            model_name='reference',
            name='unique_reference_per_user',
        ),
        migrations.RemoveConstraint(
            model_name='skill',
            name='unique_skill_per_user',
        ),
        migrations.RemoveConstraint(
            model_name='training',
            name='unique_training_per_user',
        ),
    ]
