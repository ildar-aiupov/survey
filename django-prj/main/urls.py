from django.urls import path

from main import views


app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path(
        "pass_survey/<int:survey_id>/<int:question_id>/",
        views.pass_survey,
        name="pass_survey",
    ),
    path("pass_survey/<int:survey_id>/", views.pass_survey, name="pass_survey"),
    path("delete_history", views.delete_history, name="delete_history"),
    path("show_statistics", views.show_statistics, name="show_statistics"),
]
