# Generated by Django 3.1.5 on 2022-01-02 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0041_auto_20211231_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='main',
            name='FoodGained',
            field=models.IntegerField(default=0),
        ),
    ]