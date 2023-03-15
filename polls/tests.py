import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

# test で始まる名前のファイルの中から自動的にテストを探す
# Question.was_published_recently() の過去・現在・未来の質問に対するテストを作成＝期待通りの動作を保証
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        pub_dateが現在時刻より未来に設定された場合、was_published_recently() はFalseを返さなければならない
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        # 返却値がFalseの場合、テストに通らないことを設定
        self.assertIs(future_question.was_published_recently(), False)

    # より包括的なテスト
    def test_was_published_recently_with_old_question(self):
        # 現在時刻より１日１秒前のQuestionインスタンスを作成
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)

        # 返り値がFalseの場合、テストが通る
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        # １日以内のQuestionインスタンスを作成
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def create_question(question_text, days):
        """
        引数から質問を作成する。
        例）現在から10日後の登校日の質問を作成したい場合
        create_question("hoge?", 10)
        例）10日前の質問を作成したい場合
        create_question("hoge?", -10)
        """
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question_text, pub_date=time)

# ビューに対するテストを定義
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        質問がDBにない場合、適切なメッセージが表示できているか確認する
        """
        response = self.client.get(reverse('polls:index'))

        # テストの合格条件
        # ステータスコードが200である
        self.assertEqual(response.status_code, 200)

        # コンテンツにNo polls are availableが含まれる
        self.assertContains(response, "No polls are available.")

        # DBが空であること
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        過去の投稿日の質問が一覧に表示されるか確認する
        """

        # 投稿日が30日前の質問を作成
        # ダミーデータのためメソッドが終了すればダミーデータは破棄され、DBにデータが作成されることはない
        # 新しくテストする際は質問は空の状態から始まる
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))

        # テストの合格条件
        # 投稿日30日前の質問が表示されているか確認する
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        未来の投稿日の質問が一覧に表示されていないか確認する
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))

        # テストの合格条件
        # コンテンツにNo polls are availableが含まれること
        self.assertContains(response, "No polls are available.")
        # 最新の質問５件が空なこと
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        過去・未来の質問が両方ある場合、過去の質問だけ表示される
        """
        # 過去の質問だけ変数に代入する
        # テストの合格条件を判別する際、過去質問が表示されているのを確認するため
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
       過去の質問２つが表示されているか確認する
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        detail.htmlの未来の日付のページにアクセスする場合は404を表示
        """
        # 現在から5日後の質問を作成する
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        # 合格条件
        # ページにアクセスした場合のステータスコードが404
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        過去の質問の場合はページを表示する
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)

        # 合格条件
        # ページに過去の質問が含まれている
        self.assertContains(response, past_question.question_text)