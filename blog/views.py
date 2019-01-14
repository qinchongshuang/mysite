from django.shortcuts import render, get_object_or_404

# Create your views here.
from datetime import datetime
from blog.models import BlogPost
from blog.forms import BlogPostForm
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
import markdown
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from comment.forms import CommentForm
from comment.models import Comment
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import FormView, DeleteView, CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy


class LoginRequiredMixin(View):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


# 博客列表
class BlogList(ListView):
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'  # 把查询到的queryset对象传递到模板的名字（默认为object_list）
    model = BlogPost  # 等价于queryset=BlogPost.objects.all(),指定要操作的数据模型

    def get_context_data(self, **kwargs):
        context = super(BlogList, self).get_context_data(**kwargs)
        blog_count = BlogPost.objects.all().count()
        context['blog_count'] = blog_count
        return context


# 博客搜索
class BlogSearch(BlogList):
    def get_queryset(self):
        posts = super(BlogSearch, self).get_queryset()
        self.search = self.request.GET.get('search')  # 取出request中的值
        if self.search:
            posts = posts.filter(Q(title__icontains=self.search) | Q(body__icontains=self.search))
            blog_search_count = posts.count()
            print(blog_search_count)
            self.kwargs['blog_search_count'] = blog_search_count
            return posts
        else:
            self.search = ''
            return posts

    def get_context_data(self, **kwargs):
        context = super(BlogSearch, self).get_context_data(**kwargs)
        context['search'] = self.search
        context['blog_search_count'] = self.kwargs.get('blog_search_count')
        return context


# 博客排序
class BlogOrder(BlogSearch):
    def get_queryset(self):
        posts = super(BlogOrder, self).get_queryset()
        self.order = self.request.GET.get('order')
        if self.order == 'view_nums':
            return posts.order_by('-view_nums')
        else:
            return posts

    def get_context_data(self, **kwargs):
        context = super(BlogOrder, self).get_context_data(**kwargs)
        context['order'] = self.order
        return context


# 博客分页
class BlogPaginator(BlogOrder):
    def get_queryset(self):
        posts = super(BlogPaginator, self).get_queryset()
        paginator = Paginator(posts, 2)
        page_num = self.request.GET.get('page')
        try:
            posts = paginator.page(page_num)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        return posts


# 博客创建
class BlogCreate(LoginRequiredMixin, CreateView):
    template_name = 'blog/blog_create.html'
    success_url = '/blog/'
    model = BlogPost
    fields = ['title', 'body']

    def form_valid(self, form):
        form.instance.author = self.request.user  # 获取当前的用户对象:self.request.user
        return super(BlogCreate, self).form_valid(form)


# 博客更新
class BlogUpdate(UpdateView):
    model = BlogPost
    fields = ['title', 'body']
    pk_url_kwarg = 'post_id'
    template_name = 'blog/blog_update.html'
    success_url = '/blog/'
    context_object_name = 'post'


# 博客删除
class BlogDelete(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = BlogPost.objects.get(id=post_id)
        post.delete()
        return HttpResponseRedirect('/blog/')


# 博客详情
class BlogDetail(DetailView):
    template_name = 'blog/blog_detail.html'
    model = BlogPost
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'

    def get_object(self, queryset=None):  # get_object()为DetailView独有的方法，从model中查找与pk_url_kwarg值相同的对象
        post = super(BlogDetail, self).get_object()  # get_object()默认返回一个'object'对象，重命名为post
        post.view_nums += 1
        post.save(update_fields=['view_nums'])
        self.md = markdown.Markdown(extensions=['markdown.extensions.extra',
                                                'markdown.extensions.codehilite',
                                                'toc'])
        post.body = self.md.convert(post.body)
        return post

    def get_context_data(self, **kwargs):
        context = super(BlogDetail, self).get_context_data()
        context['comments'] = self.object.comments.all()  # 反向查询
        context['toc'] = self.md.toc
        return context
