# Generated by Django 3.1.5 on 2021-08-31 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0007_square_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='main',
            name='Money',
            field=models.IntegerField(default=100),
        ),
    ]
