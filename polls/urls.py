from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('comment/', views.CommentView.as_view(), name='comment'),
    path('post_comment/', views.post_comment, name='post_comment'),
    
    # add from drf tutorial 
    path("questions/", views.get_questions, name="questions"),
    path("questions/<int:id>/", views.get_question, name="question"),
    path("questions/<int:id>/votevote/", views.votevote, name="votevote"),
    path("comments/", views.get_comments, name="comments"),
]