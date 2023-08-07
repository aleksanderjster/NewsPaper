from django import forms
from django.core.exceptions import ValidationError
from . import models
from news.models import Post, Author

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=50)  # This do the same as in commented title validation below.
    author = forms.ModelChoiceField(
        queryset = Author.objects.all(),
    )
    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'content',
            'category',
        ]

    

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')
        
        if str(title).lower() == str(content).lower():
            raise ValidationError(
                'Content and Title must be different!'
            )

        return cleaned_data
    

# customization of standard signup form save() method for allauth module.
class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
    
