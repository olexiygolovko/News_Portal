from django.views.generic import ListView, DetailView, \
    CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Post, Author, Subscribers
from .filters import NewsFilter
from .forms import NewsForm, ProfileForm, SubscribeForm

from django.contrib.auth.models import User


class NewsList(ListView):
    model = Post
    ordering = ['-dateCreation']
    template_name = 'news/news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict,
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/new.html'
    context_object_name = 'news'


class NewsSearchView(ListView):
    model = Post
    ordering = ['-dateCreation']
    template_name = 'news/search_news.html'
    context_object_name = 'news'
    paginate_by = 10
    myFilter = NewsFilter()
    context = {'myFilters': myFilter}

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class NewsCreate(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    model = Post
    template_name = 'news/news_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context

class NewsEdit(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news/news_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context

    def get_object(self, **kwargs):
        pk_id = self.kwargs.get('pk')
        return Post.objects.get(pk=pk_id)


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = '/news/'


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'profile_update.html'
    form_class = ProfileForm
    success_url = '/news/'

    def get_object(self, **kwargs):
        pk_id = self.kwargs.get('pk')
        return Post.objects.get(pk=pk_id)


class Subscribe(LoginRequiredMixin, CreateView):
    model = Subscribers
    template_name = 'news/subscribe.html'
    form_class = SubscribeForm
    success_url = '/news/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['prefix'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.subscriber = self.request.user
        return super().form_valid(form)