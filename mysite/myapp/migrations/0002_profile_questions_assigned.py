# Generated by Django 5.0.6 on 2024-06-19 06:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="questions_assigned",
            field=models.IntegerField(default=0),
        ),
    ]
