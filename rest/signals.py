from django.db.models.signals import pre_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Task

@receiver(pre_save, sender=Task)
def notification_status_updated(sender, instance, **kwargs):
    if instance.id:  # Vérifier si l'instance existe déjà (pas une création)
        try:
            old_instance = Task.objects.get(id=instance.id)
        except Task.DoesNotExist:
            return

        if old_instance.complete != instance.complete:  # Vérifier si `status` a changé
            channel_layer = get_channel_layer()
            user_id=old_instance.project.owner
            async_to_sync(channel_layer.group_send)(
                f"user_{user_id}",
                {
                    "type": "send_notification",
                    "message": f"Le statut est passé de {old_instance.complete} à {instance.complete}"
                }
            )
