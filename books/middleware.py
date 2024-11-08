from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from django.http import JsonResponse

class TokenBlacklistMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Get the token from the Authorization header
        authorization_header = request.headers.get("Authorization")
        if authorization_header:
            token = authorization_header.split(" ")[1]

            # Check if token is blacklisted
            if cache.get(f"blacklisted_{token}"):
                # Instead of raising an error we are returning a message to make it workable for right now.
                # raise AuthenticationFailed("Token is blacklisted.")

                return JsonResponse({
                    "status":False, "message":"Token is blacklisted."
                },
                status = 401
                )
        
        return None


