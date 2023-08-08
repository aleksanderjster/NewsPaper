
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, resolve
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .models import Post
from .filters import PostFilter
from .forms import PostForm
 

class PostList(ListView):
    model = Post
    queryset = Post.objects.all()
    context_object_name = 'news'
    ordering = ['-publication_date']
    template_name = 'posts.html'    
    paginate_by = 5

    def get_queryset(self):
        if self.request.path == '/news/':
            return Post.objects.filter(type='N').order_by('-publication_date')
        
        if self.request.path == '/articles/':    
             return Post.objects.filter(type='A').order_by('-publication_date')
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_not_author"] = not self.request.user.groups.filter(name='authors').exists()

        if self.request.path == '/news/':
            context['page_title'] = 'News'
            context['page_caption'] = 'Новости'
        if self.request.path == '/articles/':
            context['page_title'] = 'Articles'
            context['page_caption'] = 'Статьи'

        return context
    

class NewsSearch(ListView):
    model = Post
    queryset = Post.objects.filter(type='N')
    context_object_name = 'news'
    ordering = ['-publication_date']
    template_name = 'post_search.html'    
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'News'
        context['page_caption'] = 'Искать в новостях'
        context['filterset'] = self.filterset
        context["is_not_author"] = not self.request.user.groups.filter(name='authors').exists()

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return  self.filterset.qs


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_name = resolve(self.request.path_info).url_name

        context["is_not_author"] = not self.request.user.groups.filter(name='authors').exists()

        # from_page_number = context['from_page_number']
        if context_name == 'news_detail':
            context['page_title'] = 'News'
        if context_name == 'article_detail':
            context['page_title'] = 'Article'

        # test of request.META.HTTP_REFERER
        # print(self.request.META.get("HTTP_REFERER", context_name))
        

        return context
    
    def get_success_url(self):
        # Get the current page number from the query parameters
        current_page_number = self.request.GET.get('page', 1)

        # Create a URL for the ListView with the current_page_number as a query parameter
        list_view_url = reverse('your_model_list') + f'?page={current_page_number}'
        print(list_view_url)
        return list_view_url


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ("news.add_post",)
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


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ("news.change_post",)
    redirect_field_name = "next"
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

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ("news.delete_post",)
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
    
@login_required
def upgrade_me(request, *args, **kwargs):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    refferer = request.headers['Referer']
    
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    
    return redirect(refferer)