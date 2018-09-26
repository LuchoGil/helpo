from django.dispatch import receiver
from django.db.models import F
from django.db.models.signals import post_save
from actividades.models import Evento, ActividadesTasks, Participacion
from users.models import User, Suscripcion, OrganizacionProfile
import uuid

""" Module where all signal handlers for the Actividades app are defined """

@receiver(post_save, sender=Evento, dispatch_uid=uuid.uuid4())
def handle_evento_scheduling(sender, instance , created, **kwargs):
  
    """ Creates or updates an ActividadesTask whenever a Evento is saved """

    if created:        
        task = ActividadesTasks(tipo='EVENTO_START', execute_date=instance.fecha_hora_inicio, evento=instance)
        task.save()
    elif instance.estado == 1: # created
        task = ActividadesTasks.objects.all().filter(tipo='EVENTO_START', evento=instance)[0]
        task.execute_date = instance.fecha_hora_inicio
        task.save()
    else:
        pass


@receiver(post_save, sender=Evento, dispatch_uid=uuid.uuid4())
def handle_evento_change_notification(sender, instance, created, **kwags):
    """
    Notifica a todos los ususarios suscritos a una organizacion cuando
    esta crea o modifica un evento
    """
    # Busco la ong dueña del evento
    organizacion = User.objects.get(pk=instance.organizacion.id)
    # Busco todos los usuarios que tengo que notificar
    users = User.objects.filter(suscripcion__organizacion=organizacion)

    if created:
        for user in users:
            pass
            #Notificar cuando se crea el evento
    elif instance.estado == 1:
        # Cuando un evento creado se modifica
        for user in users:
            pass
            #Notificar modificacion de evento

@receiver(post_save, sender=Participacion, dispatch_uid=uuid.uuid4())
def handle_participacion_mano_change(sender, instance, created, **kwargs):
    """
    Actualiza la cantidad de manos de una organizacion cuando se le
    da una mano a esta en una participacion
    """    

    def sumarMano(organizacion_id):
        """
        Suma +1 a las manos de la organizacion
        """
        perfil = OrganizacionProfile.objects.get(usuario=organizcion_id)
        perfil.manos = F("manos") + 1
        perfil.save()
    
    def restarMano(organizacion_id):
        """
        Suma +1 a las manos de la organizacion
        """
        perfil = OrganizacionProfile.objects.get(usuario=organizcion_id)
        perfil.manos = F("manos") - 1
        perfil.save()

    mano_recibida = instance.retroalimentacion_ong
    organizacion_id = instance.necesidad_voluntario.evento.organizacion.id

    if (created and mano_recibida):
        sumarMano()
