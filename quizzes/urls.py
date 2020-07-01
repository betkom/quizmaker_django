from django.urls import path, re_path, include
from .api import RegisterAPI, LoginAPI, UserAPI, QuizListAPI, QuizDetailAPI, MyQuizListAPI, SaveUsersAnswer, QuizResultsAPI
from knox import views as knox_views
from knox.views import LogoutView

urlpatterns = [
  path('auth/register/', RegisterAPI.as_view()),
  path('auth/login/', LoginAPI.as_view()),
  path('auth/user/', UserAPI.as_view()),
  path('auth/logout/', knox_views.LogoutView.as_view()),
  path('my-quizzes/', MyQuizListAPI.as_view()),
  path('quizzes/', QuizListAPI.as_view()),
  re_path(r"quizzes/(?P<slug>[\w\-]+)/$", QuizDetailAPI.as_view()),
  re_path(r"quizzes/(?P<slug>[\w\-]+)/submit/$", QuizResultsAPI.as_view()),
  path("save-answer/", SaveUsersAnswer.as_view()),
]