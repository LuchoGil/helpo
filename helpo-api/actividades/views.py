from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from actividades.models import Evento, RubroEvento, CategoriaRecurso, Recurso, Necesidad, \
    Contacto, Voluntario, Funcion, Participacion, Colaboracion, Comentario, Mensaje, EventoImagen
from knox.models import AuthToken
from actividades.serializers import EventoSerializer, RubroEventoSerializer, \
    CategoriaRecursoSerializer, RecursoSerializer, NecesidadSerializer, ContactoSerializer, \
    ConsultaEventoSerializer, VoluntarioSerializer, FuncionSerializer, ConsultaNecesidadesSerializer, \
    ParticipacionSerializer, ColaboracionSerializer, ComentarioSerializer, MensajeSerializer, EventoImagenSerializer
from common.functions import get_token_user, calc_distance_locations

class RubroEventoCreateReadView(ListCreateAPIView):
    """
    API endpoint para crear o ver todos los rubros de evento
    """
    serializer_class = RubroEventoSerializer
    queryset = RubroEvento.objects.all()

class FuncionCreateReadView(ListCreateAPIView):
    """
    API endpoint para crear o ver todas las funciones de voluntariado
    """
    serializer_class = FuncionSerializer
    queryset = Funcion.objects.all()

class RubroEventoReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint para leer, actualizar o eliminar un rubro de evento
    """
    queryset = RubroEvento.objects.all()
    serializer_class = RubroEventoSerializer
    lookup_field = 'id'

class FuncionCreateReadView(ListCreateAPIView):
    """
    API endpoint para crear o ver todas las funciones de voluntariado
    """
    serializer_class = FuncionSerializer
    queryset = Funcion.objects.all()

class FuncionReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint para leer, actualizar o eliminar una función de voluntariado
    """
    queryset = Funcion.objects.all()
    serializer_class = FuncionSerializer
    lookup_field = 'id'

class ContactoEventoCreateReadView(ListCreateAPIView):
    """
    API endpoint para crear o ver todos los contactos de evento
    """
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializer

class ContactoEventoReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint para leer, actualizar o eliminar un contacto de evento
    """
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializer
    lookup_field = 'id'

class EventoCreateReadView(ListCreateAPIView):
    """
    API endpoint para crear o ver todos los eventos
    """
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer

    def create(self, request):
        serializer = EventoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organizacion_id=get_token_user(self.request))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventoReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint para leer, actualizar o eliminar un evento
    """
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        nuevo_evento = super().update(request, *args, **kwargs)
        from actividades.services import notificar_cambio_evento
        notificar_cambio_evento(request.data)
        return nuevo_evento


class CategoriaRecursoCreateReadView(ListCreateAPIView):
    """
    API endpoint para crear o ver todas las categorías de recurso
    """
    queryset = CategoriaRecurso.objects.all()
    serializer_class = CategoriaRecursoSerializer

class CategoriaRecursoReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint para leer, actualizar o eliminar una categoría de recurso
    """
    queryset = CategoriaRecurso.objects.all()
    serializer_class = CategoriaRecursoSerializer
    lookup_field = 'id'

class RecursoCreateReadView(ListCreateAPIView):
    """
    API endpoint para crear o ver todos los recursos
    """
    serializer_class = RecursoSerializer

    def get_queryset(self):
        queryset = Recurso.objects.all()
        categoria = self.request.query_params.get('categoria', None)
        if categoria is not None:
            queryset = queryset.filter(categoria_id=categoria)
        return queryset

class RecursoReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint para leer, actualizar o eliminar un recurso
    """
    queryset = Recurso.objects.all()
    serializer_class = RecursoSerializer
    lookup_field = 'id'

class NecesidadCreateReadView(ListCreateAPIView):
    """
    API endpoint para crear o ver todas las necesidades
    """
    serializer_class = NecesidadSerializer

    def get_queryset(self):
        queryset = Necesidad.objects.all()
        evento = self.request.query_params.get('evento', None)
        if evento is not None:
            queryset = queryset.filter(evento_id=evento)
        return queryset

class NecesidadReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint para leer, actualizar o eliminar una necesidad
    """
    queryset = Necesidad.objects.all()
    serializer_class = NecesidadSerializer
    lookup_field = 'id'

class VoluntarioCreateReadView(ListCreateAPIView):
    """
    API endpoint para crear o ver todas las necesidades de voluntario
    """
    serializer_class = VoluntarioSerializer

    def get_queryset(self):
        queryset = Voluntario.objects.all()
        evento = self.request.query_params.get('evento', None)
        if evento is not None:
            queryset = queryset.filter(evento_id=evento)
        return queryset

class VoluntarioReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint para leer, actualizar o eliminar una necesidad de voluntario
    """
    queryset = Voluntario.objects.all()
    serializer_class = VoluntarioSerializer
    lookup_field = 'id'


class EventoOrganizacionCreateReadView(ListCreateAPIView):
    """
    API endpoint para crear o ver todos los eventos de la organización
    """
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = EventoSerializer

    def get_queryset(self):
        queryset = Evento.objects.all()
        queryset = queryset.filter(organizacion_id=get_token_user(self.request))
        queryset = queryset.order_by('-fecha_hora_inicio')
        return queryset

class EventoVoluntarioCreateReadView(ListCreateAPIView):
    """
    API endpoint para crear o ver todos los eventos de la organización
    """
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ConsultaNecesidadesSerializer

    def get_queryset(self):
        lista_eventos = self.get_eventos(get_token_user(self.request))
        queryset = Evento.objects.all()
        queryset = queryset.filter(id__in=lista_eventos)
        return queryset

    def get_eventos(self, user):
        eventos = []
        colaboraciones = Colaboracion.objects.filter(voluntario_id=user)
        for colaboracion in colaboraciones:
            necesidad = Necesidad.objects.filter(id=colaboracion.necesidad_material_id).first()
            if necesidad.evento_id not in eventos:
                eventos.append(necesidad.evento_id)
        participaciones = Participacion.objects.filter(voluntario_id=user)
        for participacion in participaciones:
            necesidad = Voluntario.objects.filter(id=participacion.necesidad_voluntario_id).first()
            if necesidad.evento_id not in eventos:
                eventos.append(necesidad.evento_id)
        return eventos

class ConsultaEventosOrganizacionCreateReadView(ListCreateAPIView):
    """
    API endpoint para ver todos los eventos próximos
    """
    serializer_class = ConsultaEventoSerializer

    def get_queryset(self):
        queryset = Evento.objects.all()
        if 'organizacion' in self.request.query_params:
            queryset = queryset.filter(organizacion_id=self.request.query_params.get('organizacion'))
        else:
            queryset = queryset.filter(fecha_hora_inicio__gte=datetime.today())
        if 'fecha_desde' in self.request.query_params:
            queryset = queryset.filter(fecha_hora_inicio__gte=self.request.query_params.get('fecha_desde'))
            queryset = queryset.filter(fecha_hora_inicio__lte=self.request.query_params.get('fecha_hasta'))
        if 'kms' in self.request.query_params:
            kms = float(self.request.query_params.get('kms'))
            latitud = float(self.request.query_params.get('latitud'))
            longitud = float(self.request.query_params.get('longitud'))
            lista_eventos = self.filtrar_ubicacion(kms, latitud, longitud)
            queryset = queryset.filter(id__in=lista_eventos)
        if self.tiene_filtros(self.request.query_params):
            lista_eventos = self.get_eventos(self.request.query_params)
            queryset = queryset.filter(id__in=lista_eventos)
        queryset = queryset.order_by('fecha_hora_inicio')
        return queryset

    def tiene_filtros(self, params):
        filtros = ['necesidades', 'funciones', 'rubros']
        for f in filtros:
            if f in params:
                return True
        return False

    def filtrar_ubicacion(self, kms, latitud, longitud):
        eventos = Evento.objects.all()
        eventos = eventos.filter(fecha_hora_inicio__gte=datetime.today())
        ids = [e.id for e in eventos 
            if calc_distance_locations(latitud, longitud, e.ubicacion.latitud, e.ubicacion.longitud) <= kms
        ]
        return ids
    
    def get_eventos(self, params):
        eventos = []
        categorias_recurso = params.get('necesidades', None)
        if categorias_recurso is not None:
            categorias_recurso = categorias_recurso.split(',')
            for c in categorias_recurso:
                necesidades = Necesidad.objects.filter(recurso__categoria_id=c)
                for n in necesidades:
                    if n.evento_id not in eventos:
                        eventos.append(n.evento_id)
        funciones = params.get('funciones', None)
        if funciones is not None:
            funciones = funciones.split(',')
            for f in funciones:
                voluntarios = Voluntario.objects.filter(funcion__id=f)
                for v in voluntarios:
                    if v.evento_id not in eventos:
                        eventos.append(v.evento_id)
        rubros = params.get('rubros', None)
        if rubros is not None:
            rubros = rubros.split(',')
            for r in rubros:
                eventos_rubro = Evento.objects.filter(rubro__id=r)
                for e in eventos_rubro:
                    if e.id not in eventos:
                        eventos.append(e.id)
        return eventos

class ConsultaEventosReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint para leer, actualizar o eliminar un evento
    """
    queryset = Evento.objects.all()
    serializer_class = ConsultaEventoSerializer
    lookup_field = 'id'

class ColaboracionCreateReadView(ListCreateAPIView):
    """
    API endpoint para crear o ver todas las colaboraciones de voluntario
    """
    queryset = Colaboracion.objects.all()
    serializer_class = ColaboracionSerializer

    def create(self, request):
        serializer = ColaboracionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(voluntario_id=get_token_user(self.request))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ColaboracionReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint para leer, actualizar o eliminar una colaboración de voluntario
    """
    queryset = Colaboracion.objects.all()
    serializer_class = ColaboracionSerializer
    lookup_field = 'id'
    
    # de aca para abajo, es una negrada, no queda otra, preguntarle a Gon por que
    def destroy(self, request, *args, **kwargs):
        serializer = ColaboracionSerializer(data=request.data)
        colaboracion_id = request.path.split("/actividades/colaboraciones/",1)[1][:-1]
        serializer.destroy(colaboracion_id)
        return super().destroy(request, *args, **kwargs)


class ParticipacionCreateReadView(ListCreateAPIView):
    """
    API endpoint para crear o ver todas las participaciones de voluntario
    """
    queryset = Participacion.objects.all()
    serializer_class = ParticipacionSerializer

    def create(self, request):
        serializer = ParticipacionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(voluntario_id=get_token_user(self.request))
            from actividades.services import send_participacion_create_email
            send_participacion_create_email(serializer.instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParticipacionReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint para leer, actualizar o eliminar una participación de voluntario
    """
    queryset = Participacion.objects.all()
    serializer_class = ParticipacionSerializer
    lookup_field = 'id'

    # negrada is back!
    def destroy(self, request, *args, **kwargs):
        participacion_id = request.path.split("/actividades/participaciones/",1)[1][:-1]
        participacion = Participacion.objects.get(id=participacion_id)
        from actividades.services import send_participacion_destroy_email
        send_participacion_destroy_email(participacion)        
        return super().destroy(request, *args, **kwargs)


class ComentarioCreateReadView(ListCreateAPIView):
    """
    API endpoint para crear o ver todos los comentarios de evento
    """
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

    def create(self, request):
        serializer = ComentarioSerializer(data=request.data)        
        if serializer.is_valid():
            serializer.save(voluntario_id=get_token_user(self.request))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComentarioReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint para leer, actualizar o eliminar un comentario de evento
    """
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    lookup_field = 'id'

class ConsultaNecesidadesReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint para ver consultar el estado de necesidades de un evento
    """
    serializer_class = ConsultaNecesidadesSerializer
    queryset = Evento.objects.all()
    lookup_field = 'id'

@api_view(['POST'])
def RetroalimentacionVoluntarioEvento(request):
    try:
        user = get_token_user(request)
        colaboraciones = Colaboracion.objects.filter(voluntario_id=user).filter(necesidad_material__evento_id=request.data['evento'])
        for c in colaboraciones:
            c.retroalimentacion_voluntario = True
            c.save()
        participaciones = Participacion.objects.filter(voluntario_id=user).filter(necesidad_voluntario__evento_id=request.data['evento'])
        for p in participaciones:
            p.retroalimentacion_voluntario = True
            p.save()
        return Response(request.data, status=status.HTTP_201_CREATED)
    except:
       return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def RetroalimentacionONGEvento(request):
    try:
        voluntario = request.data['voluntario']
        colaboraciones = Colaboracion.objects.filter(voluntario_id=voluntario).filter(necesidad_material__evento_id=request.data['evento'])
        for c in colaboraciones:
            c.retroalimentacion_ong = True
            c.save()
        participaciones = Participacion.objects.filter(voluntario_id=voluntario).filter(necesidad_voluntario__evento_id=request.data['evento'])
        for p in participaciones:
            p.retroalimentacion_ong = True
            p.save()
        return Response(request.data, status=status.HTTP_201_CREATED)
    except:
       return Response(status=status.HTTP_400_BAD_REQUEST)

class EventoImagenRetrieveDestroyView(RetrieveDestroyAPIView):

    """ API endpoint para leer o eliminar una imagen de un evento """

    queryset = EventoImagen.objects.all()
    serializer_class = EventoImagenSerializer
    lookup_field = 'id'


class EventoImagenListView(APIView):

    """ API endpoint para ver todas las imagenes de un evento """

    def get(self, request, evento, format=None):
        print(request)
        imagenes = EventoImagen.objects.all().filter(evento=evento)
        serializer = EventoImagenSerializer(imagenes, many=True)
        return Response(serializer.data)

class EventoImagenCreateView(CreateAPIView):

    """ APU endpoint para crear una imagen de un evento """

    queryset = EventoImagen.objects.all()
    serializer_class = EventoImagenSerializer
class MensajeCreateReadView(ListCreateAPIView):
    """
    API endpoint para crear o ver todos los mensajes
    """
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = MensajeSerializer

    def get_queryset(self):
        queryset = Mensaje.objects.all()
        evento_id = self.request.query_params.get('evento', None)
        user = get_token_user(self.request)        
        if evento_id is not None:
            evento = Evento.objects.filter(id=evento_id)[0]
            if evento.organizacion_id == user:
                queryset = queryset.filter(evento_id=evento_id)
                queryset = queryset.order_by('-created')
                return queryset
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MensajeReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint para leer, actualizar o eliminar un mensaje
    """
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer
    lookup_field = 'id'
