# Generated by Django 3.2.5 on 2021-08-02 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_customuser_notification_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='notification_token',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
