from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from blog.models import BlogPost
from comment.forms import CommentForm
from django.views.generic import FormView,CreateView,View,UpdateView
from blog.views import LoginRequiredMixin
from comment.models import Comment
# Create your views here.
from django.core.urlresolvers import reverse_lazy


class CommentList(LoginRequiredMixin,CreateView):
    template_name = 'blog/blog_detail.html'
    model = Comment
    fields = ['body']
    pk_url_kwarg = 'post_id'
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = get_object_or_404(BlogPost,id=self.kwargs.get(self.pk_url_kwarg))
        return super(CommentList, self).form_valid(form)
    def get_success_url(self):
        return reverse_lazy('blog:blog_detail',
                            kwargs={'post_id':self.kwargs.get(self.pk_url_kwarg)})   # 带参数传递的success_url写法


class CommentDelete(LoginRequiredMixin,View):
    def get(self,request,comment_id):
        comment = Comment.objects.get(id=comment_id)
        post_id = comment.post_id
        comment.delete()
        return redirect('blog:blog_detail',post_id)

class CommentUpdate(LoginRequiredMixin,UpdateView):
    model = Comment
    fields = ['body']
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment_update.html'
    success_url = '/blog/'
    context_object_name = 'comment'



