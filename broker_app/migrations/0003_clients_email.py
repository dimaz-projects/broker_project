# Generated by Django 2.0.13 on 2019-06-13 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('broker_app', '0002_auto_20190528_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='clients',
            name='email',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
    ]
