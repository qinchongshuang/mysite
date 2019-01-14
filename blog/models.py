from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=150,verbose_name='标题')
    author = models.ForeignKey(User,verbose_name='作者')
    body = models.TextField(verbose_name='正文')
    create_timestamp = models.DateTimeField(auto_now_add=True)
    last_edit_timestamp = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=0)
    view_nums = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-create_timestamp',)
    def get_absolute_url(self):
        return reverse('blog:blog_detail',args=[self.id])
    # def save(self, *args,**kwargs):
    #     if not self.id:
    #         self.create_timestamp = timezone.now()
    #     self.last_edit_timestamp = timezone.now()
    #     return super(BlogPost,self).save(*args,**kwargs)



