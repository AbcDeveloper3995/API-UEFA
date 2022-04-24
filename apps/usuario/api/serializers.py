from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.usuario.models import Usuario


#EJEMPLO DE UN SERIALIZADOR QUE NO HEREDA DE UN MODELSERIALIZER POR LO QUE NO RESPONDE A UN MODELO
class testSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=100)
    email = serializers.EmailField()


    def validate_nombre(self, value):
        print(value)
        if 'dev' in value:
            raise serializers.ValidationError('Error, no se admite ese nombre')
        return value

    def validate_email(self, value):
        print(value)
        if value == '':
            raise serializers.ValidationError('Error, el email es requerido')
        return value

    def validate(self, data):
        if data['nombre'] in data['email']:
            raise serializers.ValidationError('Error, el email no puede contener el nombre')
        print('Validado')
        return data

class customTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass


class customUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email')

    def to_representation(self, instance):
        return {
            'Nombre': instance.first_name,
            'Apellidos': instance.last_name,
            'Correo': instance.email
        }

class usuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

    def validate_password(self, value):
        print(value)
        if len(value) < 8:
            raise serializers.ValidationError('La contrasena debe tener minimo 8 caracteres')
        return value


    def create(self, validated_data):
        usuario = Usuario(**validated_data)
        usuario.set_password(validated_data['password'])
        usuario.save()
        return usuario


class updateUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name')


class usuarioListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario


    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'Nombre': instance['first_name'],
            'Apellidos': instance['last_name'],
            'Nombre de usuario': instance['username'],
            'Contrase;a': instance['password'],
            'Correo': instance['email'],
            'Grupos': instance['groups__name']
        }
