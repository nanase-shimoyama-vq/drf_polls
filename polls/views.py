from django.http import HttpResponseRedirect, HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Choice, Question, Comment
import json

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # 最新の５件を取得、投稿日が現在時刻より前にある投稿のみ表示
        # Choiceを持たない質問を非公開にする
        return Question.objects.filter(pub_date__lte=timezone.now(),choice__isnull=False).distinct().order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    # どのモデルに対して動作するかを定義
    model = Question
    # どのテンプレートに表示するかを定義
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        """
        まだ公開されていない質問は除外する
        """
        # Choiceを持たない質問を非公開にする
        return Question.objects.filter(pub_date__lte=timezone.now(),choice__isnull=False).distinct()

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

class CommentView(generic.ListView):
    template_name = 'polls/comment.html'
    context_object_name = 'latest_comment_list'

    def get_queryset(self):
        return Comment.objects.order_by('-comment_date')[:5]

def post_comment(request):
    if request.POST:
        comment_text = request.POST.get("comment_text")
        model = Comment(comment_text = comment_text, comment_date = timezone.now())
        model.save()

    return HttpResponseRedirect(reverse('polls:comment'))

def get_questions(request: HttpRequest):
    questions = list(Question.objects.all().order_by("id").values())
    return JsonResponse(
        questions, safe=False, json_dumps_params={"ensure_ascii": False}
    )

def get_question(request: HttpRequest, id: int):
    question = Question.objects.get(id=id)
    response = dict()
    response["id"] = question.id
    response["question_text"] = question.question_text
    response["pub_date"] = question.pub_date
    return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})

@csrf_exempt
def votevote(request: HttpRequest, id: int):
    choice = Choice.objects.get(
        question__id=id, id=json.loads(request.body).get("choice_id")
    )
    choice.votes += 1
    choice.save()
    return HttpResponse(status=200)

def get_comments(request: HttpRequest):
    comments = list(Comment.objects.all().order_by("id").values())
    return JsonResponse(
        comments, safe=False, json_dumps_params={"ensure_ascii": False}
    )
