from django.urls import path
from .views import NewsList, NewsDetail, NewsSearchView, NewsCreate, NewsEdit, NewsDelete


urlpatterns = [
   path('', NewsList.as_view(), name='news'),
   path('<int:pk>', NewsDetail.as_view(), name='new_detail'),
   path('search/', NewsSearchView.as_view(), name='search'),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
]

