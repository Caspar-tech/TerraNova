# Generated by Django 3.1.5 on 2021-12-31 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0036_auto_20211230_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='main',
            name='NextYearBlock',
            field=models.BooleanField(default=False),
        ),
    ]
