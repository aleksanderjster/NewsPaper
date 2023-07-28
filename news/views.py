
from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .filters import PostFilter
from .forms import PostForm

# Create your views here.
class NewsList(ListView):
    model = Post
    ordering = 'publication_date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return  self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context



class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'



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


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name="post_edit.html"

class PostDelete(DeleteView):
    model=Post
    template_name="post_delete.html"
    success_url = reverse_lazy("news_list") # REMEMBER name to be given for path in urls.py
    

