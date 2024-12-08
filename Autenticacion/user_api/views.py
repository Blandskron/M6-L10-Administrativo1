from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # La vista requiere autenticación. Una vez logueado a través de /user_api/login/, se podrá acceder.
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([SessionAuthentication])
def user_api_login(request):
    """
    Este endpoint permite autenticar a un usuario contra user_api.
    Debe recibir username y password.
    Si es correcto, inicia sesión (crea la cookie de sesión) y devuelve 200.
    Si no, devuelve 400.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)  # Esto creará la sesión
        return Response({"detail": "Logged in"}, status=200)
    else:
        return Response({"detail": "Invalid credentials"}, status=400)
