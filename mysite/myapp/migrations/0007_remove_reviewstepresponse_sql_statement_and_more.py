# Generated by Django 5.0.6 on 2024-07-01 07:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0006_remove_instrchecks_creator_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="reviewstepresponse",
            name="sql_statement",
        ),
        migrations.AddField(
            model_name="question",
            name="sql_statement",
            field=models.TextField(default=""),
        ),
        migrations.AddField(
            model_name="reviewstepresponse",
            name="review_sql_statement",
            field=models.TextField(default=""),
        ),
    ]