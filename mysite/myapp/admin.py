from django.contrib import admin
from .models import (Profile, WorkedOutExample, SolutionSteps, Review, ReviewSolutionSteps,
                    DataTable, DataColumn)
# Register your models here.
admin.site.register(Profile)
admin.site.register(WorkedOutExample)
admin.site.register(SolutionSteps)
admin.site.register(Review)
admin.site.register(ReviewSolutionSteps)
admin.site.register(DataTable)
admin.site.register(DataColumn)

