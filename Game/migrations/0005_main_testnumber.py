# Generated by Django 3.1.5 on 2021-08-15 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0004_auto_20210813_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='main',
            name='Testnumber',
            field=models.IntegerField(default=0),
        ),
    ]
