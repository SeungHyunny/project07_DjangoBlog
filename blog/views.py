from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q  # 검색기능이 있는 클래스 
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic import DayArchiveView, TodayArchiveView, FormView 
from django.views.generic import ListView, DetailView, TemplateView
import requests

from blog.forms import PostSearchForm
from blog.models import Post
from mysite.views import OwnerOnlyMixin

#from django.views.generic import FormView
#--- ListView
class PostLV(ListView):
    model = Post
    template_name = 'blog/post_all.html'
    context_object_name = 'posts'
    paginate_by = 2
    
class TagCloudTV(TemplateView):
    template_name = 'taggit/taggit_cloud.html'

class TaggedObjectLV(ListView):
    template_name = 'taggit/taggit_post_list.html'
    model = Post 
    
    def get_queryset(self):
        return Post.objects.filter(tags__name = self.kwargs.get('tag'))
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context


#--- DetailView

class PostDV(DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disqus_short'] = f"{settings.DISQUS_SHORTNAME}"
        context['disqus_id'] = f"post-{self.object.id}-{self.object.slug}"
        context['disqus_url'] = f"{settings.DISQUS_MY_DOMAIN}{self.object.get_absolute_url()}"
        context['disqus_title'] = f"{self.object.slug}"
        return context

#--- ArchiveView
class PostAV(ArchiveIndexView):
    model = Post
    date_field = 'modify_dt'


class PostYAV(YearArchiveView):
    model = Post
    date_field = 'modify_dt'
    make_object_list = True


class PostMAV(MonthArchiveView):
    model = Post
    date_field = 'modify_dt'


class PostDAV(DayArchiveView):
    model = Post
    date_field = 'modify_dt'


class PostTAV(TodayArchiveView):
    model = Post
    date_field = 'modify_dt'


class SearchFormView(FormView):
    form_class = PostSearchForm
    template_name ='blog/post_search.html' 
    
    def form_valid(self,form):
        searchWord = form.cleaned_data['search_word'] 
        post_list = Post.objects.filter(
                Q(title__icontains=searchWord) |
                Q(description__icontains=searchWord) | 
                Q(content__icontains=searchWord) 
            ).distinct()
        context ={} 
        
        context['form'] = form 
        context['search_term'] = searchWord 
        context['object_list'] = post_list
        
        return render(self.request,self.template_name,context)
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'description', 'content', 'tags']
    # initial = {'slug': 'auto-filling-do-not-input'}
    success_url = reverse_lazy('blog:index')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class PostChangeLV(LoginRequiredMixin, ListView):
    template_name = 'blog/post_change_list.html'
    
    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)
    
class PostUpdateView(OwnerOnlyMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tags']
    success_url = reverse_lazy('blog:index')
    
class PostDeleteView(OwnerOnlyMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')

#crawling

class CrawlingFormView(FormView):
    template_name ='blog/post_crawling.html'
    
    def crawling(self,form):
        searchWord = form.cleaned_data['search_word']
        
        url = 'https://movie.naver.com/movie/search/result.naver?query='
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        data_list = soup.find('search_list_1')
        
        return data_list

