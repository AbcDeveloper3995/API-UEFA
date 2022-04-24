from django.db import models

CHOICE_POSICION = (
    ('', '-------'),
    ('POR', 'Portero'),
    ('DEF', 'Defensa'),
    ('LI', 'Lateral Izquierdo'),
    ('LD', 'Lateral Derecho'),
    ('MC', 'Medio Campo'),
    ('EXI', 'Extremo Izquierdo'),
    ('EXD', 'Extremo Derecho'),
    ('DEL', 'Delantero'),
)


class Liga(models.Model):
    codigo = models.IntegerField(primary_key=True, verbose_name='Codigo', unique=True, blank=False, null=False)
    descripcion = models.CharField(verbose_name='Descripcion', max_length=200, blank=False, null=False)
    pais = models.CharField(verbose_name='Pais', max_length=100, blank=True, null=True)
    esActivo = models.BooleanField(default=True)

    class Meta:
        db_table = 'Liga'
        verbose_name = 'Liga'
        verbose_name_plural = 'Ligas'
        ordering = ['codigo']

    def __str__(self):
        return '{0}--{1}'.format(str(self.descripcion), self.pais)

class Equipo(models.Model):
    fk_liga = models.ForeignKey(Liga, verbose_name='Liga', blank=True, null=True, on_delete=models.CASCADE)
    nombre = models.CharField(verbose_name='Nombre del Equipo', max_length=50, blank=False, null=False)
    ligasGanadas = models.PositiveIntegerField(verbose_name='Ligas Ganadas')
    championsGanadas = models.PositiveIntegerField(verbose_name='Champions Ganadas')
    esActivo = models.BooleanField(default=True)

    class Meta:
        db_table = 'Equipo'
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'


    def __str__(self):
        return '{0}-{1}'.format(str(self.nombre), self.fk_liga.descripcion)

class Jugador(models.Model):
    fk_equipo = models.ForeignKey(Equipo, verbose_name='Equipo del jugador', blank=True, null=True, on_delete=models.CASCADE)
    nombre = models.CharField(verbose_name='Nombre del jugador', max_length=50, blank=False, null=False)
    apellidos = models.CharField(verbose_name='Apellidos del jugador', max_length=100, blank=False, null=False)
    posicion = models.CharField(verbose_name='Posicion del jugador', max_length=100, choices=CHOICE_POSICION, blank=False, null=False)
    dorsal = models.PositiveIntegerField(verbose_name='Dorsal del jugador', blank=True, null=True)
    goles = models.PositiveIntegerField(verbose_name='Goles anotados')
    asistencias = models.PositiveIntegerField(verbose_name='Cantidad de asistencias')
    nivel = models.PositiveIntegerField(verbose_name='Nivel del jugador')
    tieneBalonDeOro = models.BooleanField(default=False)
    esTitular = models.BooleanField(default=True)
    esActivo = models.BooleanField(default=True)

    class Meta:
        db_table = 'Jugador'
        verbose_name = 'Jugador'
        verbose_name_plural = 'Jugadores'


    def __str__(self):
        return '{0}-{1}'.format(str(self.nombre), self.apellidos)