from rest_framework import viewsets, permissions
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from actividades.models import Evento, RubroEvento, CategoriaRecurso, Recurso, Necesidad, Contacto
from knox.models import AuthToken
from actividades.serializers import EventoSerializer, RubroEventoSerializer, \
    CategoriaRecursoSerializer, RecursoSerializer, NecesidadSerializer, ContactoSerializer
from common.functions import get_token_user

class RubroEventoCreateReadView(ListCreateAPIView):
    """
    API endpoint para crear o ver todos los rubros de evento
    """
    queryset = RubroEvento.objects.all()

    def create(self, request):
        serializer = RubroEventoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organizacion_id=get_token_user(self.request))
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class ContactoEventoCreateReadView(ListCreateAPIView):
    """
    API endpoint para crear o ver todos los contactos de evento
    """
    queryset = Contacto.objects.all()
    serializer_class = ContactoSerializer

class RubroEventoReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint para leer, actualizar o eliminar un rubro de evento
    """
    queryset = RubroEvento.objects.all()
    serializer_class = RubroEventoSerializer
    lookup_field = 'id'

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

class EventoReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint para leer, actualizar o eliminar un evento
    """
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    lookup_field = 'id'

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

class EventoOrganizacionCreateReadView(ListCreateAPIView):
    """
    API endpoint para crear o ver todos los eventos de la organización
    """
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = EventoSerializer

    def get_queryset(self):
        queryset = Evento.objects.all()
        queryset = queryset.filter(organizacion_id=get_token_user(self.request))
        return queryset