# Generated by Django 3.1.5 on 2021-10-21 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0022_main_gameendedsucces'),
    ]

    operations = [
        migrations.CreateModel(
            name='Highscore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.TextField(default='Anonymous')),
                ('Food', models.IntegerField(default=0)),
            ],
        ),
    ]
