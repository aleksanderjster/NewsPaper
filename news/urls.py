from django.urls import path
from news.views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, NewsSearch
from .views import upgrade_me, subscribe_to_category #, IndexView

# D11 cache_page for generics views.
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('news/', PostList.as_view(), name="news_list"),
    path('news/search/', NewsSearch.as_view(), name='search_list'),
    path('news/<int:pk>/', PostDetail.as_view(), name = 'news_detail'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path("news/<int:pk>/edit/", PostUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/', PostList.as_view(), name="article_list"),

    # D11 cache page
    # path('articles/<int:pk>/', PostDetail.as_view(), name = 'article_detail'), # ordinary generic view
    path('articles/<int:pk>/', cache_page(60*2)(PostDetail.as_view()), name = 'article_detail'), # cached generic view for 120 sec.

    path('articles/create/', PostCreate.as_view(), name='article_create'),
    path("articles/<int:pk>/edit/", PostUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('news/subscribe/<int:category>/', subscribe_to_category, name='subscribe_to_category'),
    # path('celery/', IndexView.as_view())
]
