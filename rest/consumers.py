from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """ Vérifie l'authentification et ajoute l'utilisateur à son groupe WebSocket """
        self.user = self.scope["user"]

        if self.user.is_authenticated:
            self.group_name = f"user_{self.user.id}"  # 🔥 Groupe unique pour chaque utilisateur
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close(code=403)  # 🔴 Refuse la connexion si non authentifié

    async def disconnect(self, close_code):
        """ Retire l'utilisateur de son groupe WebSocket """
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        """ Optionnel : Gérer les messages reçus par WebSocket (si besoin) """
        data = json.loads(text_data)
        message = data.get("message", "")

        # 🔥 Exemple : envoyer un message au groupe de l'utilisateur
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "send_notification",
                "message": f"Message reçu : {message}"
            }
        )

    async def send_notification(self, event):
        """ Envoie une notification à l'utilisateur """
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))
