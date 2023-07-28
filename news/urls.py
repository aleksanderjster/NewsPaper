from django.urls import path
from .views import NewsList, PostDetail, PostCreate, PostUpdate, PostDelete        # create_post

urlpatterns = [
    path('', NewsList.as_view(), name="news_list"),
    path('<int:pk>/', PostDetail.as_view(), name = 'post_detail'),
    #path('<int:pk>/', posts),
    # path('create/', create_post, name='post_create'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path("<int:pk>/update/", PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]
