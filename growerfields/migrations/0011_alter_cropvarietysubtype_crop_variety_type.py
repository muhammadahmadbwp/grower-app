# Generated by Django 3.2.5 on 2021-08-05 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('growerfields', '0010_rename_crop_variety_type_id_cropvarietysubtype_crop_variety_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cropvarietysubtype',
            name='crop_variety_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crop_variety_sub_type', to='growerfields.cropvarietytype'),
        ),
    ]
