# Generated by Django 3.1.5 on 2021-09-24 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0019_auto_20210924_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='main',
            name='Boat',
            field=models.BooleanField(default=False),
        ),
    ]