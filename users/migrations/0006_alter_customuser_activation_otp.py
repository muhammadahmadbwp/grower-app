# Generated by Django 3.2.5 on 2021-07-30 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_customuser_activation_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='activation_otp',
            field=models.IntegerField(default=8796, verbose_name='activation otp'),
        ),
    ]