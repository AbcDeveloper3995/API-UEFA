from django.db.models import Sum
from django.db.models.functions import Coalesce

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.uefa.api.serializers import *


class ligaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ligaSerializer
    list_serializer_class = listarLigaSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.list_serializer_class.Meta.model.objects.filter(esActivo=True).values('codigo', 'descripcion')
        return self.serializer_class.Meta.model.objects.filter(codigo=pk).first()

    def list(self, request, *args, **kwargs):

        """Documentacion para listar jugadores

           Aca encontrara lo necesario a tener en cuenta para la funcionalidad de listar jugadores"""
        serializer = self.list_serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Liga creada correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Liga modificada correctamente', 'data': serializer.data},
                                status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Liga no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        liga = self.get_queryset(pk)
        if liga:
            liga.esActivo = False
            liga.save()
            return Response({'message': 'liga eliminada correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'liga no encontrada'}, status=status.HTTP_400_BAD_REQUEST)


class equipoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = equipoSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.serializer_class.Meta.model.objects.filter(esActivo=True)
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()

    def list(self, request, *args, **kwargs):
        print(request.user.get_all_permissions())
        permisos = list(request.user.get_all_permissions())
        if 'uefa.view_equipo' in permisos:
            print('permiso encontrado')
        else:
            print('permiso no encontrado')
        message = f'{request.user.first_name} usted no tiene los permisos requerido para realizar esta accion.'
        data = {'error': message}
        if request.user.has_perm('uefa.view_equipo'):
            serializer = self.serializer_class(self.get_queryset(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Equipo creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Equipo modificado correctamente', 'data': serializer.data},
                                status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Equipo no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        equipo = self.get_queryset(pk)
        if equipo:
            equipo.esActivo = False
            equipo.save()
            return Response({'message': 'Equipo eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Equipo no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='obtener-delanteros')
    def getDelanteros(self, request, *args, **kwargs):
        data = {}
        equipo = self.serializer_class.Meta.model.objects.filter(id=self.kwargs['pk']).first()
        delanteros = Jugador.objects.filter(posicion='DEL', fk_equipo=equipo)
        serializer = jugadorSerializer(delanteros, many=True)
        data = {'equipo': equipo.nombre, 'delanteros': serializer.data}
        return Response({'message': 'Delanteros', 'data': data}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['get'], url_path='cantidad-jugadores')
    def cantidadDeJugadores(self, request, *args, **kwargs):
        data, aux = {}, []
        equipos = self.serializer_class.Meta.model.objects.all()
        for i in equipos:
            cantjugadores = Jugador.objects.filter(fk_equipo=i).count()
            data = {'Equipo': i.nombre, 'Cantidad de jugadores': cantjugadores}
            aux.append(data)
        return Response({'message': 'Cantidad de jugadores por equipo.', 'data': aux}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['get'], url_path='titulares-por-equipo')
    def titularesDeCadaEquipo(self, request, *args, **kwargs):
        data, aux = {}, []
        equipos = self.serializer_class.Meta.model.objects.all()
        for i in equipos:
            jugadores = Jugador.objects.filter(fk_equipo=i, esTitular=True)
            serializer = titularSerializer(jugadores, many=True)
            data = {'equipo': i.nombre, 'titulares': serializer.data}
            aux.append(data)
        return Response({'message': 'Jugadores titulares por equipo.', 'data': aux}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='nivel-cada-plantilla')
    def nivelDePlantillasTitulares(self, request, *args, **kwargs):
        data, aux = {}, []
        equipos = self.serializer_class.Meta.model.objects.all()
        for i in equipos:
            nivel = Jugador.objects.filter(fk_equipo=i, esTitular=True).aggregate(nivel=Coalesce(Sum('nivel'), 0)).get(
                'nivel')
            data = {'Equipo': i.nombre, 'Nivel de la plantilla': nivel}
            aux.append(data)
        return Response({'message': 'Nivel de cada plantilla.', 'data': aux}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='mejor-plantilla')
    def equipoDeMejorPlantilla(self, request, *args, **kwargs):
        data, aux = {}, 0
        equipos = self.serializer_class.Meta.model.objects.all()
        for i in equipos:
            nivel = Jugador.objects.filter(fk_equipo=i, esTitular=True).aggregate(nivel=Coalesce(Sum('nivel'),0)).get('nivel')
            if nivel > aux:
                aux = nivel
                data = {'Equipo': i.nombre, 'Nivel de la': nivel}
        return Response({'message': 'Plantilla con mas nivel.', 'data': data}, status=status.HTTP_200_OK)


class jugadorViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = jugadorSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.serializer_class.Meta.model.objects.filter(esActivo=True)
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()


    def list(self, request, *args, **kwargs):
        jugador_serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(jugador_serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        jugador_serializer = self.serializer_class(data=request.data)
        if jugador_serializer.is_valid():
            jugador_serializer.save()
            return Response({'message': 'Jugador creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(jugador_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            jugador_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if jugador_serializer.is_valid():
                jugador_serializer.save()
                return Response({'message': 'Jugador modificado correctamente', 'data': jugador_serializer.data},
                                status=status.HTTP_202_ACCEPTED)
            return Response(jugador_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Jugador no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        jugador = self.get_queryset(pk)
        if jugador:
            jugador.esActivo = False
            jugador.save()
            return Response({'message': 'Jugador eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Jugador no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='rango-nivel')
    def jugadoresConNivelEntre8_10(self, request, *args, **kwargs):
        jugadores = self.serializer_class.Meta.model.objects.filter(nivel__range=(8, 10), esTitular=True)
        serializers = titularSerializer(jugadores, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


