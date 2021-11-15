# Generated by Django 3.2.5 on 2021-08-05 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagemodel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='timestamp'),
        ),
        migrations.AlterField(
            model_name='messagemodel',
            name='deleted_by_recipient',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='timestamp'),
        ),
        migrations.AlterField(
            model_name='messagemodel',
            name='deleted_by_user',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='timestamp'),
        ),
        migrations.AlterField(
            model_name='messagemodel',
            name='message',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='messagemodel',
            name='recipient',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL, verbose_name='recipient'),
        ),
        migrations.AlterField(
            model_name='messagemodel',
            name='seen_at',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='timestamp'),
        ),
    ]
