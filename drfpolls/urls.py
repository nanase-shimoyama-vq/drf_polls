from django.urls import include, path
from rest_framework import routers
from .views import QuestionList, QuestionControl, ChoiceList, CommentList, CommentControl

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("questions/", QuestionList.as_view()),
    path("questions/<int:pk>/", QuestionControl.as_view(), name="question-control"),
    path("choices/", ChoiceList.as_view()),
    path("comments/", CommentList.as_view(), name="comment-list"),    
    path("comments/<int:pk>/", CommentControl.as_view(), name="comment-control"),
]