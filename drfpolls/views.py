from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import QuestionSerializer, ChoiceSerializer, CommentSerializer
from .models import Question, Choice, Comment

class QuestionList(APIView):

    def get(self, request, format=None):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = QuestionSerializer(data = request.data)
        if serializer.is_valid():
            Question.objects.create(
                id = serializer.data.get("id"),
                question_text = serializer.data.get("question_text"),
                pub_date = serializer.data.get("pub_date"),
            )
            question = Question.objects.all().filter(id=request.data["id"]).values()
            return Response(question, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionControl(APIView):

    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404
  
    def get(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
 
    def put(self, request, pk):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    def delete(self, request, pk):
        question = self.get_object(pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ChoiceList(APIView):

    def get(self, request):
        choices = Choice.objects.all()
        serializer = ChoiceSerializer(choices, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        c_serializer = ChoiceSerializer(data = request.data)
        if c_serializer.is_valid():
            Choice.objects.create(
                id = c_serializer.data.get("id"),
                choice_text = c_serializer.data.get("choice_text"),
                votes = c_serializer.data.get("votes"),
                question_id = c_serializer.data.get("question_id"),
            )
            question = Choice.objects.all().filter(id=request.data["id"]).values()
            return Response(question, status=status.HTTP_201_CREATED)
        
        return Response(c_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChoiceControl(APIView):

    def get_object(self, pk):
        try:
            return Choice.objects.get(pk=pk)
        except Choice.DoesNotExist:
            raise Http404
  
    def get(self, request, pk, format=None):
        choice = self.get_object(pk)
        serializer = ChoiceSerializer(choice)
        return Response(serializer.data)
 
    def put(self, request, pk):
        choice = self.get_object(pk)
        serializer = ChoiceSerializer(choice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    def delete(self, request, pk):
        choice = self.get_object(pk)
        choice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentList(APIView):
    # serializer = CommentSerializer

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid():
            Comment.objects.create(
                id = serializer.data.get("id"),
                comment_text = serializer.data.get("comment_text"),
                comment_date = serializer.data.get("comment_date"),
            )
            comment = Comment.objects.all().filter(id=request.data["id"]).values()
            return Response(comment, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentControl(APIView):

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404
  
    def get(self, request, pk, format=None):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
 
    def put(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    def delete(self, request, pk):
        comment = self.get_object(pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)