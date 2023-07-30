
from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from news.models import Post
# from .filters import PostFilter
from news.forms import PostForm

# Create your views here.
class ArticleList(ListView):
    model = Post
    queryset = Post.objects.filter(type='A')
    ordering = 'publication_date'
    template_name = 'posts.html'
    context_object_name = 'articles'
    paginate_by = 10

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = PostFilter(self.request.GET, queryset)
    #     return  self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['filterset'] = self.filterset
        context['page_title'] = 'Articles'
        context['page_caption'] = 'Статьи'
        return context



class ArticleDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Article'
        return context



# def create_post(request):
#     form = PostForm()
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/news/')
#     return render(request, 'post_edit.html', {'form': form})


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name="post_edit.html"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = "A"
        return super().form_valid(form)


class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name="post_edit.html"

class ArticleDelete(DeleteView):
    model=Post
    template_name="post_delete.html"
    success_url = reverse_lazy("article_list") # REMEMBER name to be given for path in urls.py
    

