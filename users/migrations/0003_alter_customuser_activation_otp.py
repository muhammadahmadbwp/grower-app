# Generated by Django 3.2.5 on 2021-07-28 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210728_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='activation_otp',
            field=models.IntegerField(default=5657, verbose_name='activation otp'),
        ),
    ]
