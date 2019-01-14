from django.db import models
from django.contrib.auth.models import User
from blog.models import BlogPost
from django.core.urlresolvers import reverse

class Comment(models.Model):
    post = models.ForeignKey(BlogPost,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    body = models.TextField()
    create_timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-create_timestamp',)
    def __str__(self):
        return self.body[:20]