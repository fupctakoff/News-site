from django.shortcuts import render, redirect
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout


class HomeNews(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    extra_context = {'title': 'Список новостей'}
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['count'] = News.objects.filter(is_published=True).count()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'
    allow_empty = False

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsByCategory, self).get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context


class GetNew(DetailView):
    model = News
    pk_url_kwarg = 'new_id'
    template_name = 'news/new.html'
    context_object_name = 'new'

    def get_context_data(self, **kwargs):
        context = super(GetNew, self).get_context_data(**kwargs)
        try:
            context['previous_new'] = self.get_object().get_previous_by_created_at(is_published=True)
        except:
            print('Невозможно взять предыдущий объект')
        try:
            context['next_new'] = self.get_object().get_next_by_created_at(is_published=True)
        except:
            print('Невозможно взять следующий объект')
        return context


class CreateNew(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_new.html'
    raise_exception = True


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Успешная регистрация')
            return redirect('home')
        else:
            messages.error(request, 'Неудачная регистрация')
    else:
        form = UserRegisterForm()

    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Успешная аутентификация')
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')
