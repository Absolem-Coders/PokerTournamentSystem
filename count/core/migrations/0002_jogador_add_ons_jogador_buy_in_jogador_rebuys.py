# Generated by Django 5.0.1 on 2024-02-01 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jogador',
            name='add_ons',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='jogador',
            name='buy_in',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='jogador',
            name='rebuys',
            field=models.IntegerField(default=0),
        ),
    ]
