from django.urls import path
from articles.views import ArticleList, ArticleDetail, ArticleCreate, ArticleUpdate, ArticleDelete

urlpatterns = [
    path('', ArticleList.as_view(), name="article_list"),                 # refers to /articles/ as initial page
    path('<int:pk>/', ArticleDetail.as_view(), name = 'article_detail'),
    path('create/', ArticleCreate.as_view(), name='article_create'),
    path("<int:pk>/update/", ArticleUpdate.as_view(), name='article_update'),
    path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]
