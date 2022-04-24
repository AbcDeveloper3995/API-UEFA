from django.contrib import admin
from django.contrib.auth.models import Permission

from apps.usuario.models import Usuario


class usuarioAdmin( admin.ModelAdmin):
    list_display = ('id', 'first_name','last_name', 'username', 'is_superuser', 'is_active')


admin.site.register(Usuario, usuarioAdmin)
admin.site.register(Permission)

