# Generated by Django 3.1.5 on 2021-09-17 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0015_main_textevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='main',
            name='EventButton1',
            field=models.TextField(default='B1'),
        ),
        migrations.AddField(
            model_name='main',
            name='EventButton2',
            field=models.TextField(default='B2'),
        ),
    ]
