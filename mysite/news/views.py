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
        context['count'] = News.objects.filter(is_published=True).count()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True)


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


class CreateNew(CreateView):
    form_class = NewsForm
    template_name = 'news/add_new.html'
