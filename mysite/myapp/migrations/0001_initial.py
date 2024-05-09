# Generated by Django 5.0.3 on 2024-04-11 18:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('project_description', models.TextField()),
                ('project_context', models.TextField()),
                ('data_table_description', models.TextField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_examples', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_instructor', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('example', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='myapp.example')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('order', models.IntegerField(help_text='The order of the step within the question')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='myapp.question')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('example', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='myapp.example')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(choices=[('completely_disagree', 'Completely Disagree'), ('disagree', 'Disagree'), ('neutral', 'Neutral'), ('agree', 'Agree'), ('completely_agree', 'Completely Agree')], max_length=50)),
                ('free_response', models.TextField(blank=True, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='myapp.question')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='myapp.review')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewStepResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sql_statement', models.TextField()),
                ('question_step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_responses', to='myapp.questionstep')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='step_responses', to='myapp.review')),
            ],
        ),
    ]
