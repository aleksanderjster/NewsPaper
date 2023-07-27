from django import forms
from django.core.exceptions import ValidationError

from .models import Post

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=50)  # This do the same as in commented title validation below.

    class Meta:
        model = Post
        fields = [
            'author',
            'type',
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