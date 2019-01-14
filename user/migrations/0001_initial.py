# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('phone', models.CharField(verbose_name='电话', max_length=20, blank=True)),
                ('avatar', models.ImageField(verbose_name='头像', blank=True, upload_to='avatar/%Y%m%d/')),
                ('bio', models.TextField(verbose_name='简介', max_length=500, blank=True)),
                ('user', models.OneToOneField(related_name='userpro', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
