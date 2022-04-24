# Generated by Django 3.2.7 on 2022-04-18 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uefa', '0002_auto_20220417_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipo',
            name='championsGanadas',
            field=models.PositiveIntegerField(verbose_name='Champions Ganadas'),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='ligasGanadas',
            field=models.PositiveIntegerField(verbose_name='Ligas Ganadas'),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='nombre',
            field=models.CharField(max_length=50, verbose_name='Nombre del Equipo'),
        ),
        migrations.AlterField(
            model_name='jugador',
            name='asistencias',
            field=models.PositiveIntegerField(verbose_name='Cantidad de asistencias'),
        ),
        migrations.AlterField(
            model_name='jugador',
            name='goles',
            field=models.PositiveIntegerField(verbose_name='Goles anotados'),
        ),
        migrations.AlterField(
            model_name='jugador',
            name='nivel',
            field=models.PositiveIntegerField(verbose_name='Nivel del jugador'),
        ),
    ]
