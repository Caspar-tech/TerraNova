# Generated by Django 3.1.5 on 2021-10-21 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0023_highscore'),
    ]

    operations = [
        migrations.AddField(
            model_name='main',
            name='GameEndedHighscore',
            field=models.BooleanField(default=False),
        ),
    ]
