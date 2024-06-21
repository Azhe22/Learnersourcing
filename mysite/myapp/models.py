from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_instructor = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    questions_assigned = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Example(models.Model):
    # id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='created_examples')
    title = models.CharField(max_length=255)
    project_description = models.TextField()
    project_context = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} by {self.creator.user.username}"


class DataTable(models.Model):
    example = models.ForeignKey(Example, on_delete=models.CASCADE, related_name='data_tables')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} in {self.example.title}"


class DataColumn(models.Model):
    data_table = models.ForeignKey(DataTable, on_delete=models.CASCADE, related_name='columns')
    name = models.CharField(max_length=255)
    data_type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} in {self.data_table.name}"


class Question(models.Model):
    example = models.ForeignKey(Example, on_delete=models.CASCADE, related_name='questions')
    order = models.IntegerField(help_text="The order of the question within the example")
    text = models.TextField()

    class Meta:
        ordering = ['order']


class QuestionStep(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='steps')
    description = models.TextField()
    order = models.IntegerField(help_text="The order of the step within the question")

    class Meta:
        ordering = ['order']


class Review(models.Model):
    example = models.ForeignKey(Example, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews')
    problem_context_like = models.TextField(default="")
    problem_context_suggestions = models.TextField(default="")
    recommendation_likelihood = models.TextField(default="")
    appropriateness_class = models.TextField(default="")
    class Meta:
        unique_together = ('example', 'reviewer')

class ReviewStepResponse(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='step_responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='review_responses')
    sql_statement = models.TextField()
    # Add more fields as necessary for step response


class ReviewQuestion(models.Model):
    question_text = models.TextField()
    response_type = models.CharField(max_length=20, choices=[
        ('rating', 'Rating'),
        ('free_response', 'Free Response'),
    ])

    def __str__(self):
        return f"Review Question: {self.question_text[:50]}..."


class ReviewQuestionResponse(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='feedbacks')
    question = models.ForeignKey(ReviewQuestion, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.CharField(max_length=50, choices=[
        ('completely_disagree', 'Completely Disagree'),
        ('disagree', 'Disagree'),
        ('neutral', 'Neutral'),
        ('agree', 'Agree'),
        ('completely_agree', 'Completely Agree'),
    ])
    free_response = models.TextField(blank=True, null=True)


class AssignedReview(models.Model):
    example = models.ForeignKey(Example, on_delete=models.CASCADE, related_name='assigned_reviews')
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='assignments')
    assigned_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.example.title} assigned to {self.reviewer.user.username}"
    


class ProblemTable(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='created_problems')
    project_context = models.TextField()
    project_description = models.TextField()
    provided_solution = models.TextField()
    problem_type = models.CharField(max_length=255, default="Pl/SQL")
    self_review = models.FloatField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    student_reviewed = models.BooleanField(default=False)
    instr_reviewed = models.BooleanField(default=False)
    no_student_reviews = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} by {self.creator.user.username}"

class SolnTable(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='created_solutions')
    problem = models.ForeignKey(ProblemTable, on_delete=models.CASCADE, related_name='solutions')
    solution = models.TextField()
    completed = models.BooleanField(default=False)
    review_score = models.FloatField(default=0)
    review = models.TextField()
    is_review = models.BooleanField(default=False)

class InstrChecks(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='created_checks')
    problem_id = models.IntegerField()
    student_id = models.IntegerField()
    is_question = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    review_score = models.FloatField(default=0)
    review = models.TextField()


