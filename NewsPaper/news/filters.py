from django_filters import FilterSet, ModelMultipleChoiceFilter, ChoiceFilter, CharFilter, DateFilter
from django.forms.widgets import DateInput
from .models import Post, Author


class NewsFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        super(NewsFilter, self).__init__(*args, **kwargs)
        auth = []
        for names in Author.objects.all().order_by('authorUser__username').values('id', 'authorUser__username'):
            auth.append((names.get('id'), names.get('authorUser__username')))
        self.filters['author'].extra.update(
            {
                'choices': auth
            }
        )

    # You can also make multiple selections for the author.:
    # author = ModelMultipleChoiceFilter(
    #     field_name='author',
    #     queryset=Author.objects.all(),
    #     label='Author',
    #     conjoined=False,
    # )

    author = ChoiceFilter(
        field_name='author',
        label="Author's name",
        empty_label='All'
    )

    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Article title'
    )

    data = DateFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='Published no earlier',
        widget=DateInput(format='%d.%m.%Y',
                         attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ('author', 'title', 'data')