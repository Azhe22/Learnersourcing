from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    instructor = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    questions_assigned = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class WorkedOutExample(models.Model):
    # id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='created_examples')
    title = models.CharField(max_length=255)
    problem_description = models.TextField()
    problem_context = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    submitted = models.BooleanField(default=False)
    student_reviews = models.IntegerField(default=0) #number
    instructor_reviews = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} by {self.creator.user.username}"


class DataTable(models.Model):
    example = models.ForeignKey(WorkedOutExample, on_delete=models.CASCADE, related_name='data_tables')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} in {self.example.title}"


class DataColumn(models.Model):
    data_table = models.ForeignKey(DataTable, on_delete=models.CASCADE, related_name='columns')
    name = models.CharField(max_length=255)
    data_type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} in {self.data_table.name}"


class SolutionSteps(models.Model):
    example = models.ForeignKey(WorkedOutExample, on_delete=models.CASCADE, related_name='questions')
    order = models.IntegerField(help_text="The order of the question within the example")
    text = models.TextField()
    sql_statement = models.TextField(default="")
    class Meta:
        ordering = ['order']



class Review(models.Model): #Actual Review which stores the 4 review comments
    example = models.ForeignKey(WorkedOutExample, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews')
    how_much_do_you_like_example = models.TextField(default="")
    constructive_suggestions = models.TextField(default="")
    how_likely_are_you_to_recommend_example = models.IntegerField(default=0)
    #appropriateness_class = models.TextField(default="") #Only needed for instructor review
    class Meta:
        unique_together = ('example', 'reviewer')

class ReviewSolutionSteps(models.Model): #Stores the reviewer's answer/solution
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='step_responses')
    question = models.ForeignKey(SolutionSteps, on_delete=models.CASCADE, related_name='review_responses')
    review_sql_statement = models.TextField(default="")

class InstrReviews(models.Model): #Needs development
    example = models.ForeignKey(WorkedOutExample, on_delete=models.CASCADE, related_name='instr_reviews')
    submitted = models.BooleanField(default=False) #submitted
    review_score = models.FloatField(default=0)
    review = models.TextField()


