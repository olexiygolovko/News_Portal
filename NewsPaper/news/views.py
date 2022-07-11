from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    ordering = ['-dateCreation']
    template_name = 'news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'news'

