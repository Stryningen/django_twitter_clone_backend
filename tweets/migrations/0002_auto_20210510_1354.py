# Generated by Django 3.2.2 on 2021-05-10 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='tweet_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='tweet_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
