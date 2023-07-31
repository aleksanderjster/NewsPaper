from django.urls import path
from news.views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete        # create_post

urlpatterns = [
    path('news/', PostList.as_view(), name="news_list"),
    path('news/<int:pk>/', PostDetail.as_view(), name = 'news_detail'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path("news/<int:pk>/edit/", PostUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/', PostList.as_view(), name="article_list"),
    path('articles/<int:pk>/', PostDetail.as_view(), name = 'article_detail'),
    path('articles/create/', PostCreate.as_view(), name='article_create'),
    path("articles/<int:pk>/edit/", PostUpdate.as_view(), name='article_update'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
]
