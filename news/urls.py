from django.urls import path
from news.views import NewsList, NewsDetail, NewsCreate, NewsUpdate, NewsDelete        # create_post

urlpatterns = [
    path('', NewsList.as_view(), name="news_list"),
    path('<int:pk>/', NewsDetail.as_view(), name = 'news_detail'),
    #path('<int:pk>/', posts),
    # path('create/', create_post, name='post_create'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path("<int:pk>/edit/", NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
]
