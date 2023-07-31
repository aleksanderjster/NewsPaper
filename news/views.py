
from typing import Any, Optional
from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Post
# from .filters import PostFilter
from .forms import PostForm
from django.urls import resolve
   

# Create your views here.
class PostList(ListView):
    model = Post

    # queryset = Post.objects.filter(type='N')
    queryset = Post.objects.all()
    context_object_name = 'news'

    ordering = ['-publication_date']
    template_name = 'posts.html'
    
    paginate_by = 10

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = PostFilter(self.request.GET, queryset)
    #     return  self.filterset.qs


    def get_queryset(self):
        if self.request.path == '/news/':
            return Post.objects.filter(type='N').order_by('-publication_date')
        
        if self.request.path == '/articles/':    
             return Post.objects.filter(type='A').order_by('-publication_date')
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_page_number = self.request.GET.get('page', 1)
        context['from_page_number'] = int(current_page_number)
        print(current_page_number)

# def get(self, request, *args, **kwargs):
#         # Get the current page number from the query parameters
#         current_page_number = self.request.GET.get('page', 1)

#         # Store the current_page_number in the session
#         request.session['current_page_number'] = current_page_number

#         return super().get(request, *args, **kwargs)

# class YourModelDetailView(DetailView):
#     model = YourModel
#     template_name = 'your_detail_template.html'
#     context_object_name = 'your_model'

#     def get_success_url(self):
#         # Retrieve the current_page_number from the session
#         current_page_number = self.request.session.get('current_page_number', 1)

#         # Redirect to the YourModelListView with the current_page_number as a query parameter
#         return f"/list/?page={current_page_number}"

        if self.request.path == '/news/':
            context['page_title'] = 'News'
            context['page_caption'] = 'Новости'
        if self.request.path == '/articles/':
            context['page_title'] = 'Articles'
            context['page_caption'] = 'Статьи'
        
        return context



class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_name = resolve(self.request.path_info).url_name

        # from_page_number = context['from_page_number']
        if context_name == 'news_detail':
            context['page_title'] = 'News'
        if context_name == 'article_detail':
            context['page_title'] = 'Article'
        return context
    
    def get_success_url(self):
        # Get the current page number from the query parameters
        current_page_number = self.request.GET.get('page', 1)

        # Create a URL for the ListView with the current_page_number as a query parameter
        list_view_url = reverse('your_model_list') + f'?page={current_page_number}'
        print(list_view_url)
        return list_view_url



# def create_post(request):
#     form = PostForm()
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/news/')
#     return render(request, 'post_edit.html', {'form': form})


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name="post_edit.html"

    def form_valid(self, form):
        post = form.save(commit=False)
        context_name = resolve(self.request.path_info).url_name

        if context_name == 'news_create':
            post.type = "N"
        if context_name == 'article_create':
            post.type = "A"
        
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_name = resolve(self.request.path_info).url_name

        if context_name == 'news_create':
            context['page_title'] = 'News'
            context['page_caption'] = 'Создать новость'
        if context_name == 'article_create':
            context['page_title'] = 'Articles'
            context['page_caption'] = 'Создать статью'
        

        return context


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name="post_edit.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_name = resolve(self.request.path_info).url_name

        if context_name == 'news_update':
            context['page_title'] = 'News'
            context['page_caption'] = 'Редактировать новость'
        if context_name == 'article_update':
            context['page_title'] = 'Article'
            context['page_caption'] = 'Редактировать статью'

        return context

class PostDelete(DeleteView):
    model=Post
    template_name="post_delete.html"
    # success_url = reverse_lazy("news_list") # REMEMBER name to be given for path in urls.py

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_name = resolve(self.request.path_info).url_name

        if context_name == 'news_delete':
            context['page_title'] = 'News'
            context['page_caption'] = 'Удаление новости'

        if context_name == 'article_delete':
            context['page_title'] = 'Article'
            context['page_caption'] = 'Удаление статьи'


        return context
    
    def get_success_url(self):
        # Get the name of the current URL pattern
        current_url_name = self.request.resolver_match.url_name

        # You can now use a conditional statement to set the success_url based on the URL name
        if current_url_name == 'news_delete':  # Replace with your URL name
            return reverse('news_list')  # Replace with the success view URL name
        elif current_url_name == 'article_delete':  # Replace with another URL name
            return reverse('article_list')  # Replace with another success view URL name

        # Default fallback URL
        return super().get_success_url()
    

