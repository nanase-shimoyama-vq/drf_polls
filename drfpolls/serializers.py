from rest_framework import serializers

from .models import Question, Comment, Choice

# syrializerの種類、メソッド

class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label="Enter id")
    question_text = serializers.CharField(label="Enter quetions")
    pub_date = serializers.DateTimeField(label="pub_date")

    class Meta:
        model = Question
        fields = ["id", "question_text", "pub_date"]
        depth = 1

class ChoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label="Enter id")
    choice_text = serializers.CharField(label="Enter choice")

    class Meta:
        model = Choice
        fields = "__all__"
        depth = 1

class CommentSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(label="Enter id")
    comment_text = serializers.CharField(label="Enter comment")
    comment_date = serializers.DateTimeField(label="Comment date")

    class Meta:
        model = Comment
        fields = "__all__"