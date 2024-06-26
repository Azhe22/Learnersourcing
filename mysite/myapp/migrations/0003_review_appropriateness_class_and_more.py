# Generated by Django 5.0.6 on 2024-06-19 12:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0002_profile_questions_assigned"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="appropriateness_class",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="review",
            name="problem_context_like",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="review",
            name="problem_context_suggestions",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="review",
            name="recommendation_likelihood",
            field=models.TextField(default=""),
        ),
    ]
