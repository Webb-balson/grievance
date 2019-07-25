from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
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

@login_required
@user_passes_test(lambda u: u.is_superuser)
def division_topics(request, pk):
    division = get_object_or_404(Division, pk=pk)
    topics = division.topics.order_by('-last_updated').annotate(replies=Count('complains') - 1)
    return render(request, 'topics.html', {'division': division, 'topics': topics})

@login_required
def division_topics_user(request, pk):
    division = get_object_or_404(Division, pk=pk)
    user = request.user
    topics_user = division.topics.filter(starter = request.user).order_by('-last_updated').annotate(replies=Count('complains') - 1)
    return render(request, 'topics_user.html', {'division': division, 'topics_user': topics_user})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def topic_complains(request, pk, topic_pk):
    topic = get_object_or_404(Topic, division__pk=pk, pk=topic_pk)
    topic.save()
    return render(request, 'topic_complains.html', {'topic': topic})

def complain_details(request, pk, topic_pk):
    topic = get_object_or_404(Topic, division__pk=pk, pk=topic_pk)
    topic.save()
    return render(request, 'complain_details.html', {'topic': topic})


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
            return redirect('complain_details', pk=pk, topic_pk=topic.pk)
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
            topic.last_updated = timezone.now()
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


