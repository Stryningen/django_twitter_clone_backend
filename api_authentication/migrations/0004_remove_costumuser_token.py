# Generated by Django 3.2.3 on 2021-07-05 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_authentication', '0003_alter_costumuser_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='costumuser',
            name='token',
        ),
    ]
