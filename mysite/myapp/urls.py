from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sign_in", views.sign_in, name="sign_in"),
    path("expert", views.expert, name="expert"),
    path("explorer", views.explore, name="explorer"),
    path("review", views.review_menu, name="review"),
    path("review/<int:example_id>", views.review, name="review_example"),
    path("new_workout", views.new_workout, name="new_workout"),
    path("logout", views.logout_view, name="logout"),
]
