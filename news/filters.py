from django_filters import FilterSet, DateFilter, CharFilter, ChoiceFilter
from django.forms import DateInput
from news.models import Post, Author
# we create filter set for our model Post

class AuthorChoiceFilter(ChoiceFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('choices', self.get_author_choices())
        super().__init__(*args, **kwargs)

    def get_author_choices(self):
        # Get all distinct authors' usernames from the User model and create a list of choices
        authors = Author.objects.values_list('user__username', flat=True).distinct()
        return [(author, author) for author in authors]

class PostFilter(FilterSet):
    author = AuthorChoiceFilter(
        field_name='author__user__username',
        label='По автору',
        empty_label='Выбрать автора'
    )
    title = CharFilter(
        lookup_expr='icontains', 
        label='По заголовку')
    content = CharFilter(
        lookup_expr='icontains', 
        label='По заголовку')
    publication_date = DateFilter(
        field_name="publication_date", 
        lookup_expr='gte',
        widget = DateInput(attrs={
            "type": "date",
            }),
        label='По дате'
        )
    
    class Meta:
        model = Post
        fields = ['author','title', "content", "publication_date"]
