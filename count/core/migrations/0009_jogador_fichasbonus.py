# Generated by Django 5.0.1 on 2024-02-12 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_torneio_intervalo_ativo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jogador',
            name='fichasbonus',
            field=models.IntegerField(default=0),
        ),
    ]
