# Generated by Django 5.0.3 on 2024-04-25 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imdb', '0002_alter_movie_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.CharField(max_length=100),
        ),
    ]
