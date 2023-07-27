from django_filters import FilterSet
from .models import Post

# we create filter set for our model Post
class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'title': ['contains'],
            'content': ['contains'],
            # 'category': ['contains'],
            # 'publication_date': [
            #     'gt',
            #     'lt',
            # ],
            # 'rating': ['gt'],
        }