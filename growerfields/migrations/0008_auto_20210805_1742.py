# Generated by Django 3.2.5 on 2021-08-05 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('growerfields', '0007_auto_20210731_0313'),
    ]

    operations = [
        migrations.AddField(
            model_name='growerfieldmodel',
            name='area_unit',
            field=models.CharField(default='acre', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='growerfieldmodel',
            name='field_name',
            field=models.CharField(default='test field', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='growerfieldmodel',
            name='field_status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'ratoon'), (2, 'planted')], default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='growerfieldmodel',
            name='land_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'owned'), (2, 'leased')], default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='growerfieldmodel',
            name='multi_fields',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
