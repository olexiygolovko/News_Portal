from django.views.generic import ListView, DetailView, \
    CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.core.cache import cache
from django.utils.translation import gettext as _
from django.shortcuts import redirect, render

import logging
import pytz

from .models import Post, Author, Subscribers
from .filters import NewsFilter
from .forms import NewsForm, ProfileForm, SubscribeForm



logger = logging.getLogger('news.views')


class NewsList(ListView):
    model = Post
    ordering = ['-dateCreation']
    template_name = 'news/news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        # We receive a regular request
        queryset = super().get_queryset()
        # Let's use our filtering class.
        # self.request.GET contains an object QueryDict,
        # We save our filtering in a class object,
        # so that you can then add it to the context and use it in the template.
        self.filterset = NewsFilter(self.request.GET, queryset)
        #Returning a filtered list of products from the function
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add a filtering object to the context.
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/new.html'
    context_object_name = 'news'

    def get_object(self, *args, **kwargs):  # override the object receiving method, oddly enough

        obj = cache.get(f'news-{self.kwargs["pk"]}',
                        None)  # a cache is very similar to a dictionary, and the get method works the same way. It takes the value by key, if it does not exist, then it takes None.

        # if the object is not in the cache, then we get it and write it to the cache
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
        # Add a filtering object to the context.
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
    logger.info(f'the article has been changed')

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
    logger.info(f'the article has been delete')

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



def set_timezone(request):
    if request.method == 'POST':
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')
    else:
        return render(request, 'template.html', {'timezones': pytz.common_timezones})