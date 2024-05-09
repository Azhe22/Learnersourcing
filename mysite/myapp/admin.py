from django.contrib import admin
from .models import (Profile, Example, Question, QuestionStep, Review, ReviewStepResponse, ReviewQuestionResponse,
                     AssignedReview, ReviewQuestion, DataTable, DataColumn)
# Register your models here.
admin.site.register(Profile)
admin.site.register(Example)
admin.site.register(Question)
admin.site.register(QuestionStep)
admin.site.register(Review)
admin.site.register(ReviewStepResponse)
admin.site.register(ReviewQuestionResponse)
admin.site.register(AssignedReview)
admin.site.register(ReviewQuestion)
admin.site.register(DataTable)
admin.site.register(DataColumn)

