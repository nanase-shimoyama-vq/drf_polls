from rest_framework import serializers

from polls.models import Question, Comment

# syrializerの種類、メソッド

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "question_text", "pub_date"]
        # read_only_fields = ["choices"]
        depth = 1

class CommentSerializer(serializers.ModelSerializer):
    # Metaを詳しく調べてみよう
    class Meta:
        model = Comment
        # fieldsを詳しく調べてみよう
        # fields = ["id", "comment_text", "comment_date"]
        exclude = ["id"]
        depth = 1