# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('izin', '0008_pengajuanizin'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pemohon',
            options={'ordering': ['-status', 'id'], 'verbose_name': 'Pemohon', 'verbose_name_plural': 'Pemohon'},
        ),
        migrations.AddField(
            model_name='pemohon',
            name='created_by',
            field=models.ForeignKey(related_name='create_pemohon_by_user', verbose_name=b'Dibuat Oleh', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='pemohon',
            name='rejected_at',
            field=models.DateTimeField(null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='pemohon',
            name='rejected_by',
            field=models.ForeignKey(related_name='rejected_pemohon_by_user', verbose_name=b'Dibatalkan Oleh', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='pemohon',
            name='verified_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 8, 13, 3, 59, 50, 157860, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pemohon',
            name='verified_by',
            field=models.ForeignKey(related_name='verify_pemohon_by_user', verbose_name=b'Diverifikasi Oleh', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
