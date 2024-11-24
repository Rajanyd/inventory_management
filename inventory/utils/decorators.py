from functools import wraps
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import redirect

# def jwt_required(view_func):
#     @wraps(view_func)
#     def _wrapped_view(request, *args, **kwargs):
#         auth_header = request.META.get('HTTP_AUTHORIZATION', None)
#         if not auth_header or not auth_header.startswith('Bearer '):
#             return redirect('login')  # Redirect to login if token is missing/invalid
        
#         token = auth_header.split(' ')[1]  # Extract the token
        
#         jwt_auth = JWTAuthentication()
#         try:
#             validated_token = jwt_auth.get_validated_token(token)
#             request.user = jwt_auth.get_user(validated_token)  # Attach user to request
#             return view_func(request, *args, **kwargs)
#         except AuthenticationFailed:
#             return redirect('login')  # Redirect to login on authentication failure

#     return _wrapped_view


def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.COOKIES.get('access_token')
        if not token:
            return redirect('login')  # Redirect to login if no token
        
        jwt_auth = JWTAuthentication()
        try:
            validated_token = jwt_auth.get_validated_token(token)
            request.user = jwt_auth.get_user(validated_token)
            return view_func(request, *args, **kwargs)
        except AuthenticationFailed:
            return redirect('login')
    return _wrapped_view

