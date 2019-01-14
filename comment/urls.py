
from django.conf.urls import url
from comment import views
from comment.views import CommentList,CommentDelete,CommentUpdate



urlpatterns = [
    # url(r'^comment(?P<post_id>\d*)$',views.post_comment,name='post_comment'),
    url(r'^blog_comment(?P<post_id>\d*)$',CommentList.as_view(),name='blog_comment'),
    url(r'^comment_delete(?P<comment_id>\d*)$',CommentDelete.as_view(),name='comment_delete'),
    url(r'^comment_update(?P<comment_id>\d*)$',CommentUpdate.as_view(),name='comment_update'),
]
