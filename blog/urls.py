from django.conf.urls import url
from blog.views import BlogCreate, BlogList, BlogPaginator, BlogDetail, BlogDelete, BlogUpdate
from blog import views

urlpatterns = [
    url(r'^$', BlogPaginator.as_view(), name='blog_list'),
    url(r'^blog_create$', BlogCreate.as_view(), name='blog_create'),
    url(r'^blog_update(?P<post_id>\d*)$', BlogUpdate.as_view(), name='blog_update'),
    url(r'^blog_delete(?P<post_id>\d*)$', BlogDelete.as_view(), name='blog_delete'),
    url(r'^blog_detail(?P<post_id>\d*)$', BlogDetail.as_view(), name='blog_detail'),
]
