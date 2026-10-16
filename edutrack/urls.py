from . import views
from .views import obtenir_profil
from django.contrib.auth.models import User
from django.urls import path
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
  username = request.data.get('username')
  password = request.data.get('password')
  email = request.data.get('email', '')

  if not username or not password:
    return Response(
        {'error': 'Le nom d’utilisateur et le mot de passe sont requis.'},
        status=status.HTTP_400_BAD_REQUEST,
    )

  if User.objects.filter(username=username).exists():
    return Response(
        {'error': 'Ce nom d’utilisateur est déjà pris.'},
        status=status.HTTP_400_BAD_REQUEST,
    )

  user = User.objects.create_user(
      username=username, password=password, email=email
  )
  return Response(
      {'message': 'Utilisateur créé avec succès.'},
      status=status.HTTP_201_CREATED,
  )

urlpatterns = [
    path('register/', register_view, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('projets/', views.ProjetListCreateView.as_view()),
    path('projets/<int:id>/', views.ProjetRetrieveUpdateDestroyView.as_view()),
    path('taches/', views.TacheListCreateView.as_view()),
    path('taches/<int:id>/', views.TacheRetrieveUpdateDestroyView.as_view()),
    path('sous_taches/', views.SousTacheListCreateView.as_view()),
    path('sous_taches/<int:id>/', views.SousTacheRetrieveUpdateDestroyView.as_view()),
    path('profil/', obtenir_profil, name='obtenir_profil'),
]
