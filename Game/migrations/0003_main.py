# Generated by Django 3.1.5 on 2021-08-13 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0002_auto_20210803_2150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Main',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.TextField(default='Game')),
                ('Rows', models.IntegerField(default=5)),
                ('Colums', models.IntegerField(default=5)),
            ],
        ),
    ]