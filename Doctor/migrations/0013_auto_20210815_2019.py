# Generated by Django 3.2 on 2021-08-15 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0012_auto_20210815_2016'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activehour',
            name='user',
        ),
        migrations.AddField(
            model_name='activehour',
            name='userid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
