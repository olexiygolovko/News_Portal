from .views import NewsList, NewsDetail, NewsSearchView, NewsCreate, NewsEdit, NewsDelete, Subscribe
from django.urls import path
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(NewsList.as_view()), name='news'),
    path('<int:pk>', NewsDetail.as_view(), name='new_detail'),
    path('search/', NewsSearchView.as_view(), name='search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('subscribe/', Subscribe.as_view(), name='subscribe'),
]
