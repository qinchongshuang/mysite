from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserPro(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='userpro')
    phone = models.CharField(max_length=20,blank=True,verbose_name='电话')
    avatar = models.ImageField(upload_to='avatar/%Y%m%d/',blank=True,verbose_name='头像')
    bio = models.TextField(max_length=500,blank=True,verbose_name='简介')
    def __str__(self):
        return 'user{}'.format(self.user.username)

@receiver(post_save,sender=User)
def create_user_userpro(sender,instance,created,**kwargs):
    if created:
        UserPro.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_user_userpro(sender,instance,**kwargs):
    instance.userpro.save()
