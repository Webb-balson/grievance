# Generated by Django 2.2.3 on 2019-07-21 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('divisions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
