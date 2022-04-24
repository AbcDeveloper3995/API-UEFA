from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.usuario.api.serializers import *


class testApiView(APIView):
    def get(self, request):
        testData = {'nombre': 'anthuan', 'email':'anthuan@gmail.com'}
        test_serializer = testSerializer(data=testData)
        if test_serializer.is_valid():
            return Response({'message':'Todo validado'},status=status.HTTP_200_OK)
        else:
            return Response(test_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(TokenObtainPairView):
    serializer_class = customTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        usuario = authenticate(username=username, password=password)
        if usuario:
            login_serializers = self.serializer_class(data=request.data)
            if login_serializers.is_valid():
                usuario_serializer = customUsuarioSerializer(usuario)
                return Response({
                    'token': login_serializers.validated_data.get('access'),
                    'refresh-token': login_serializers.validated_data.get('refresh'),
                    'usuario': usuario_serializer.data,
                    'message': 'Inicio de sesion exitoso.'
                }, status=status.HTTP_200_OK)
            return Response({'error': login_serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Contrasena o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)


class Logout(GenericAPIView):

    def post(self, request, *args, **kwargs):
        usuario = Usuario.objects.filter(id=request.data.get('usuario', 0))
        if usuario.exists():
            RefreshToken.for_user(usuario.first())
            return Response({'message':'Se ha cerrado su sesion.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_400_BAD_REQUEST)


class usuarioViewSet(viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated,)
    model = Usuario
    serializer_class = usuarioSerializer
    list_serializer_class = usuarioListarSerializer
    queryset = None

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.filter(is_active=True).values('id', 'first_name', 'last_name', 'username','password', 'email', 'groups__name')
        return self.queryset

    def list(self, request):
        usuarios = self.get_queryset()
        serializer = self.list_serializer_class(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        usuario = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(usuario)
        return Response({'message': 'Detalles del usuario', 'data': serializer.data}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
         usuario = self.get_object(pk)
         serializer = updateUsuarioSerializer(usuario, data=request.data)
         if serializer.is_valid():
             if usuario.password != request.data['password']:
                 usuario.set_password(request.data['password'])
                 usuario.save()
             serializer.save()
             return Response({'message': 'Usuario actualizado correctamente'}, status=status.HTTP_201_CREATED)
         return Response({'message': 'Ha ocurrido un error en la actualizacion', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        usuario = self.model.objects.filter(id=pk).update(is_active=False)
        if usuario == 1:
            return Response({'message': 'Usuario eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Usuario no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='get-permisos')
    def getPermisos(self, request, *args, **kwargs):
        usuario = self.model.objects.filter(id=self.kwargs['pk']).first()
        return Response({'grupos': usuario.groups.all().values('name'),
                         'permisos asignados': usuario.get_group_permissions()}, status=status.HTTP_200_OK)
