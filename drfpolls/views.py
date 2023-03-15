from urllib.request import Request
from django.http import HttpResponse
from rest_framework import viewsets
from polls.models import Question, Comment
from drfpolls.serializers import QuestionSerializer, CommentSerializer
from rest_framework.decorators import action

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(detail=True, methods=["post"])
    def votevote(self, request: Request, *args, **kwargs):
        question = self.get_object()
        choice_id = request.data.get("choice_id")  # type: ignore
        choice = question.choices.get(id=choice_id)
        choice.votes = choice.votes
        choice.save()

        return HttpResponse(status=200)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    