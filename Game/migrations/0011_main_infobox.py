# Generated by Django 3.1.5 on 2021-09-02 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0010_main_price_discover_tile'),
    ]

    operations = [
        migrations.AddField(
            model_name='main',
            name='Infobox',
            field=models.TextField(default='hello there-second line-third line'),
        ),
    ]
