from django.contrib import admin

from apps.uefa.models import *


class ligaAdmin(admin.ModelAdmin):
    search_fields = ['codigo']
    list_display = ('codigo', 'descripcion', 'pais', 'esActivo')

class equipoAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    list_display = ('id','nombre', 'ligasGanadas', 'championsGanadas', 'fk_liga', 'esActivo')

class jugadorAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    list_display = ('id', 'nombre', 'apellidos', 'fk_equipo', 'dorsal', 'posicion', 'nivel', 'esTitular',  'esActivo')



admin.site.register(Liga, ligaAdmin)
admin.site.register(Equipo, equipoAdmin)
admin.site.register(Jugador, jugadorAdmin)
