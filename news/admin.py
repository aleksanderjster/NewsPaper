from django.contrib import admin
from .models import Post, Category

# Register your models here.

def reset_rating(ModelAdmin, request, queryset):
    queryset.update(rating=0)
    reset_rating.short_description = 'reset rating'


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'preview', 'author' ,'publication_date', 'rating']
    list_filter = ('author', 'publication_date')
    search_fields = ('title', 'content')
    actions = [reset_rating]

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
