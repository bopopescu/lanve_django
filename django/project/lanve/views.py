from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render

from django.urls import reverse_lazy
from django.views import generic

from .admin import UserCreationForm
from .forms import IssueCreateForm
from .models import Issue


# Create your views here.

class WelcomeView(generic.TemplateView):
    template_name = 'lanve/welcome.html'


class SignupView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('lanve:signin')

    def post(self, request, *args, **kwargs):
        response = super().post(self)
        # messages.success(self.request, 'Your account was created successfully')
        return response


class ListView(generic.ListView, LoginRequiredMixin):
    model = Issue  # make html file name as model name + list.html
    paginate_by = 100
    login_url = 'lanve:signin'

    def get_queryset(self):
        queryset = Issue.objects.all().order_by('-created_at')  # 新しい投稿順
        # keyword = self.request.GET.get('keyword')
        # if keyword:
        #     queryset = queryset.filter(
        #         Q(title__icontains=keyword) | Q(text__icontains=keyword)
        #
        #     )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AddView(LoginRequiredMixin, generic.CreateView):
    model = Issue
    form_class = IssueCreateForm
    login_url = 'lanve:signin'

    # 単純なフォームだったらform_classはいらなくてこれでok
    # fields = '__all__'

    # redirect()はhttp response objectを返す関数
    # reverse_lazy()は文字列を返す関数
    success_url = reverse_lazy('lanve:list')

    def form_valid(self, form):
        messages.success(self.request, 'Your issue was posted successfully')
        issue = form.save(commit=False)
        form.instance.user = self.request.user
        user = form.instance.user
        issue.contributor = user
        issue.save()
        response = super().form_valid(form)
        return response


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Issue
    login_url = 'lanve:signin'

