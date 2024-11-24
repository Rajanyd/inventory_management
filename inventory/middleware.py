from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import redirect

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('access_token')
        if token:
            try:
                # Check if the token is valid
                access_token = AccessToken(token)
                request.user = access_token.payload['user_id']  # Set the user from the token payload
            except Exception as e:
                request.user = None  # Invalid token
        else:
            request.user = None  # No token found
        response = self.get_response(request)
        return response
