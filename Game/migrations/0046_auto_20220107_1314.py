# Generated by Django 3.1.5 on 2022-01-07 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0045_auto_20220107_1309'),
    ]

    operations = [
        migrations.RenameField(
            model_name='main',
            old_name='FoodLost',
            new_name='WarFoodLost',
        ),
        migrations.RenameField(
            model_name='main',
            old_name='PopulationKilled',
            new_name='WarPopulationLost',
        ),
        migrations.RenameField(
            model_name='main',
            old_name='TilesUndiscovered',
            new_name='WarTilesLost',
        ),
    ]
