import os

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator

from django.urls import reverse
from django.views import generic
from django.utils import timezone


from .models import Question, Choice
from .forms import ChoiceForm, ImageForm

# Create your views here.
UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/polls/files/'


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'


    """
    以下を書くことで、ログインしていない場合はログイン画面にリダイレクトされるようになる
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)    
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        """Return the last five published questions."""
        # filter関数で、ログインしたユーザーのQuestionのみ習得する
        return Question.objects.all().filter(pub_date__lte=timezone.now())\
                                     .filter(user_id=self.request.user)\
                                     .order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)
        ctx['choice_form'] = ChoiceForm()
        ctx['image_form'] = ImageForm()

        total = 0
        choice_list = []

        # 総数を算出
        for choice in Choice.objects.filter(question=self.kwargs.get('pk')):

            total += choice.votes

        # choice_listにvotesと割合を算出して代入
        for choice in Choice.objects.filter(question=self.kwargs.get('pk')):

            tmp = dict()
            tmp['choice_text'] = choice.choice_text
            tmp['votes'] = choice.votes
            tmp['rate'] = choice.votes / total

            choice_list.append(tmp)

        ctx["choice_list"] = choice_list
        ctx["total"] = total


        return ctx

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



@login_required
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


@login_required
def add_choice(request, question_id):
    """
    detailから送信されたフォームを元にchoiceにデータを追加する関数
    """

    choice = Choice()
    choice.question = get_object_or_404(Question, pk=question_id)
    choice.choice_text = request.POST['choice_text']
    choice.votes = 0

    choice.save()

    return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))


@login_required
def upload_image(request, question_id):
    """
    detailから送信されたフォームを元に画像を保存する関数

    参考:
    https://qiita.com/narupo/items/e3dbdd5d030952d10661
    """

    # フォームのフォーマットに従ってデータを整形する
    form = ImageForm(request.POST, request.FILES)
    # 画像を登録するquestionを習得する
    question = get_object_or_404(Question, pk=question_id)

    if not form.is_valid():
        raise ValueError('invalid form')

    question.image_url = form.cleaned_data['image']
    question.save()

    # detailにリダイレクトする
    return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))
