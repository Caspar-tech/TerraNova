# Generated by Django 3.1.5 on 2021-08-26 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0006_square_discovered'),
    ]

    operations = [
        migrations.AddField(
            model_name='square',
            name='Number',
            field=models.IntegerField(default=0),
        ),
    ]
