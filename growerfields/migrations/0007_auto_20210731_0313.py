# Generated by Django 3.2.5 on 2021-07-30 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('growerfields', '0006_auto_20210730_0722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldcoordsbygrowermodel',
            name='latitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='fieldcoordsbygrowermodel',
            name='longitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='fieldcoordsbysurveyormodel',
            name='latitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='fieldcoordsbysurveyormodel',
            name='longitude',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='growerfieldmodel',
            name='area_auto',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='growerfieldmodel',
            name='area_manual',
            field=models.FloatField(),
        ),
    ]
