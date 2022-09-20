from django.views.generic import ListView, DetailView, \
    CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.core.cache import cache
import logging

logger = logging.getLogger('news.views')



from .models import Post, Author, Subscribers
from .filters import NewsFilter
from .forms import NewsForm, ProfileForm, SubscribeForm


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

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно

        obj = cache.get(f'news-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'news-{self.kwargs["pk"]}', obj)

        return obj


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
    permission_required = ('news.add_post',)
    model = Post
    template_name = 'news/news_edit.html'
    context_object_name = 'news_create'
    form_class = NewsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context

    def get_object(self, **kwargs):
        pk_id = self.kwargs.get('pk')
        return Post.objects.get(pk=pk_id)


class NewsEdit(LoginRequiredMixin, UpdateView):
    form_class = NewsForm
    model = Post
    permission_required = ('news.change_post',)
    template_name = 'news/news_edit.html'
    context_object_name = 'news_edit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context

    def get_object(self, **kwargs):
        pk_id = self.kwargs.get('pk')
        return Post.objects.get(pk=pk_id)


class NewsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = '/news/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'news/profile_update.html'
    form_class = ProfileForm
    success_url = '/news/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(authorUser=request.user)
        logger.info(f'User {user} join the "authors" group.')
    return redirect('/news/')


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
