# Generated by Django 3.1.5 on 2021-09-10 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0011_main_infobox'),
    ]

    operations = [
        migrations.RenameField(
            model_name='main',
            old_name='Money',
            new_name='Food',
        ),
    ]
