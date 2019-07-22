from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from .forms import NewComplainForm, ComplainForm
from .models import Division, Topic, Complain

class DivisionListView(ListView):
    model = Division
    context_object_name = 'divisions'
    template_name = 'home.html'

class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs['division'] = self.division
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.division = get_object_or_404(Division, pk=self.kwargs.get('pk'))
        queryset = self.division.topics.order_by('-last_updated').annotate(replies=Count('complains') - 1)
        return queryset

class ComplainListView(ListView):
    model = Complain
    context_object_name = 'complains'
    template_name = 'topic_complains.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)  # <-- here
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True 
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, division__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.complains.order_by('created_at')
        return queryset

@login_required
def new_complain(request, pk):
    division = get_object_or_404(Division, pk=pk)
    if request.method == 'POST':
        form = NewComplainForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.division = division
            topic.starter = request.user
            topic.save()
            complain = Complain.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_complains', pk=pk, topic_pk=topic.pk)
    else:
        form = NewComplainForm()
    return render(request, 'new_complain.html', {'division': division, 'form': form})

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, division__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = ComplainForm(request.POST)
        if form.is_valid():
            complain = form.save(commit=False)
            complain.topic = topic
            complain.created_by = request.user
            complain.save()
            topic.last_updated = timezone.now()  # <- here
            topic.save() 
            topic_url = reverse('topic_complains', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=complain.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_post_url)
    else:
        form = ComplainForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


# @method_decorator(login_required, name='dispatch')
# class UserUpdateView(UpdateView):
#     model = User
#     fields = ('first_name', 'last_name', 'email', )
#     template_name = 'my_account.html'
#     success_url = reverse_lazy('my_account')

#     def get_object(self):
#         return self.request.user
