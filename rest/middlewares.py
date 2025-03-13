from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):
    """ Middleware pour authentifier WebSocket avec JWT """
    
    async def __call__(self, scope, receive, send):
        print("hi")  # Vérification que le middleware est exécuté
        query_string = parse_qs(scope["query_string"].decode())  
        token = query_string.get("token", [None])[0]  
        scope["user"] = AnonymousUser()  

        if token:
            try:
                access_token = AccessToken(token)  
                user = await database_sync_to_async(User.objects.get)(id=access_token["user_id"])  
                scope["user"] = user
            except Exception as e:
                print("Erreur JWT :", e)

        return await self.inner(scope, receive, send)  # ⬅️ Corrige l'erreur ici
