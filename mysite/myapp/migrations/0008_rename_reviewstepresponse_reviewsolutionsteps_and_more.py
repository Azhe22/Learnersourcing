# Generated by Django 5.0.6 on 2024-07-02 06:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0007_remove_reviewstepresponse_sql_statement_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ReviewStepResponse",
            new_name="ReviewSolutionSteps",
        ),
        migrations.RenameModel(
            old_name="Question",
            new_name="SolutionSteps",
        ),
        migrations.RenameModel(
            old_name="Example",
            new_name="WorkedOutExample",
        ),
        migrations.RenameField(
            model_name="review",
            old_name="problem_likeness",
            new_name="how_much_do_you_like_example",
        ),
        migrations.RemoveField(
            model_name="review",
            name="appropriateness_class",
        ),
        migrations.RemoveField(
            model_name="review",
            name="recommendation_likelihood",
        ),
        migrations.AddField(
            model_name="review",
            name="how_likely_are_you_to_recommend_example",
            field=models.IntegerField(default=0),
        ),
    ]
