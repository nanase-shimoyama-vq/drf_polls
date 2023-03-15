from django.urls import include, path
from rest_framework import routers
from drfpolls import views

router = routers.DefaultRouter()
router.register(r"questions", views.QuestionViewSet)
router.register(r"comments", views.CommentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]