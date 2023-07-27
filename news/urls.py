from django.urls import path
from .views import NewsList, PostDetail, create_post

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>/', PostDetail.as_view(), name = 'post_detail'),
    #path('<int:pk>/', posts),
    path('create/', create_post, name='post_create'),
]
