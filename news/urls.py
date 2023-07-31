from django.urls import path
from news.views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete        # create_post

urlpatterns = [
    path('news/', PostList.as_view(), name="news_list"),
    path('<int:pk>/', PostDetail.as_view(), name = 'news_detail'),
    #path('<int:pk>/', posts),
    # path('create/', create_post, name='post_create'),
    path('create/', PostCreate.as_view(), name='news_create'),
    path("<int:pk>/edit/", PostUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/', PostList.as_view(), name="article_list"),
]
