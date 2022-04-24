from rest_framework import serializers

from apps.uefa.models import *

class listarLigaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liga
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'Codigo': instance['codigo'],
            'Nombre de la liga': instance['descripcion']
                }

class ligaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liga
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'Codigo': instance.codigo,
            'Nombre de la liga': instance.descripcion,
            'Pais': instance.pais,
                }

    def validate_pais(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError({'pais': 'Este campo es requerido, no puede estar en blanco.'})
        return value

    def validate(self, data):
        if 'pais' not in data.keys():
            raise serializers.ValidationError({'pais': 'No se encontro el campo llamado pais.'})
        return data


class equipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'Nombre del equipo': instance.nombre,
            'Liga a la que pertenece': instance.fk_liga.descripcion
                }

    def validate_nombre(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError({'pais': 'Este campo es requerido, no puede estar en blanco.'})
        return value

    def validate(self, data):
        if 'fk_liga' not in data.keys():
            raise serializers.ValidationError({'liga': 'No se encontro el campo llamado fk_liga.'})

        query = Equipo.objects.filter(fk_liga__codigo=data['fk_liga'].codigo, nombre__icontains=data['nombre'])
        if query:
            raise serializers.ValidationError({'nombre': 'Ya existe un equipo con ese nombre en esta liga.'})

        return data

class jugadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jugador
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'Nombre': instance.nombre,
            'Apellidos': instance.apellidos,
            'Equipo': instance.fk_equipo.nombre,
            'Posicion principal': instance.posicion,
            'Goles en la temporada': instance.goles,
            'Asistencias en la temporada': instance.asistencias,
            'Posee balones de oro': instance.tieneBalonDeOro,
            'Es titular': instance.esTitular
                }
    def validate_fk_equipo(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError({'fk_equipo': 'Este campo es requerido, no puede estar en blanco.'})
        return value

    def validate(self, data):
        if 'fk_equipo' not in data.keys():
            raise serializers.ValidationError({'fk_equipo': 'No se encontro el campo llamado fk_equipo.'})

        if 'dorsal' not in data.keys():
            raise serializers.ValidationError({'dorsal': 'No se encontro el campo llamado dorsal.'})

        query = Jugador.objects.filter(fk_equipo__id=data['fk_equipo'].id, dorsal=data['dorsal'])
        if query:
            message = 'Ya existe un jugador en el {} con es dorsal.'.format(data['fk_equipo'].nombre)
            raise serializers.ValidationError({'dorsal': message})
        return data


class titularSerializer(serializers.Serializer):
    titulares = serializers.CharField(max_length=100)

    def to_representation(self, instance):
        return {
            'nombre': instance.nombre,
            'apellidos': instance.apellidos,
            'nivel': instance.nivel,
                }





