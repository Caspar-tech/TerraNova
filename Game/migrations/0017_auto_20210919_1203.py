# Generated by Django 3.1.5 on 2021-09-19 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0016_auto_20210917_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='main',
            name='EndEvent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='main',
            name='StartEvent',
            field=models.BooleanField(default=False),
        ),
    ]
