# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('izin', '0011_auto_20160315_0856'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='izin',
            name='user',
        ),
        migrations.AddField(
            model_name='izin',
            name='create_by',
            field=models.ForeignKey(related_name='izin_create_by', default=1, verbose_name=b'Dibuat Oleh', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
