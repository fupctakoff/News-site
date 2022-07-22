from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse
from .models import News, Category
from .forms import NewsForm
from django.views.generic import ListView, DetailView, CreateView


class HomeNews(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    extra_context = {'title': 'Список новостей'}
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True)


# def index(request):
#     news = News.objects.order_by('-created_at')
#     context = {
#         'news': news,
#         'title': 'Новости',
#     }
#     return render(request, 'news/index.html', context=context)

class NewsByCategory(ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'
    allow_empty = False

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsByCategory, self).get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context


# def get_category(request, category_id):
#     news = get_list_or_404(News, category_id=category_id)
#     # news = News.objects.filter(category_id=category_id) --- альтернативная версия строки выше, только без 404 статус кода
#     category = get_object_or_404(Category, pk=category_id)
#     # category = Category.objects.get(pk=category_id)  --- альтернативная версия строки выше, только без 404 статускода
#     return render(request, template_name='news/category.html',
#                   context={'news': news, 'category': category, 'title': 'Новости', }, )


class GetNew(DetailView):
    model = News
    pk_url_kwarg = 'new_id'
    template_name = 'news/new.html'
    context_object_name = 'new'

# def get_new(request, new_id):
#     new = get_object_or_404(News, pk=new_id)
#     return render(request, template_name='news/new.html', context={'new': new})


class CreateNew(CreateView):
    form_class = NewsForm
    template_name = 'news/add_new.html'

# def add_new(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             new_new = form.save()
#             return redirect('new', new_new.pk)
#     else:
#         form = NewsForm()
#     return render(request, template_name='news/add_new.html',
#                   context={'form': form, })
