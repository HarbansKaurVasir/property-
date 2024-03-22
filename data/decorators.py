from functools import wraps
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
def check_credentials(view_func):
    @wraps(view_func)
    def wrapper(view_instance, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user_type = request.data.get('user_type')
        
        if not email or not password or not user_type:
            return Response({'error': 'Email, password, and user_type are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.filter(email=email, password=password, user_type=user_type).exists()
        if user is not None:
            request.user = user  # Set the authenticated user in the request
            return view_func(view_instance, request, *args, **kwargs)
        else:
            return Response({'error': 'Invalid credentials or user is not found.'}, status=status.HTTP_401_UNAUTHORIZED)

    return wrapper