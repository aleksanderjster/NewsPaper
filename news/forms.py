from django import forms
from django.core.exceptions import ValidationError
from . import models
from news.models import Post, Author

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=50)  # This do the same as in commented title validation below.
    author = forms.ModelChoiceField(
        queryset = Author.objects.all(),
    )
    # author = forms.ModelMultipleChoiceField(
    #     queryset=models.Author.objects.all().values("user__username"),
    #     select= 
    #     widget=forms.Select
    # )
    class Meta:
        model = Post
        fields = [
            'author',
            # 'type',
            'title',
            'content',
            'category',
        ]

    

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        # if title is not None and len(title) > 50:
        #     raise ValidationError({
        #         'title': 'Title can not be more than 50 symbols'
        #     })
        
        if str(title).lower() == str(content).lower():
            raise ValidationError(
                'Content and Title must be different!'
            )

        return cleaned_data