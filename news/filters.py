from django_filters import FilterSet, ModelChoiceFilter
from .models import Post    # , POST_TYPE

# we create filter set for our model Post
class PostFilter(FilterSet):
    # type = ModelChoiceFilter(
    #     label = 'Тип публикации',
    #     empty_label = 'Все'
    # )
    class Meta:
        model = Post
        fields = {
            # 'title': ['icontains'],
            # 'content': ['icontains'],
            'type',
            # 'publication_date': [
            #     'gt',
            #     'lt',
            # ],
            # 'rating': ['gt'],
        }