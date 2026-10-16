from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtenir_profil(request):
  user = request.user
  return Response({
      'username': user.username,
      'email': user.email,
  })

class ProjetListCreateView(generics.ListCreateAPIView):
  serializer_class = ProjetSerializers
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    return Projet.objects.filter(user=self.request.user)

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

class ProjetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = ProjetSerializers
  permission_classes = [IsAuthenticated]
  lookup_field = 'id'

  def get_queryset(self):
    return Projet.objects.filter(user=self.request.user)

class TacheListCreateView(generics.ListCreateAPIView):
  serializer_class = TacheSerializers
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    queryset = Tache.objects.filter(projet__user=self.request.user)
    projet_id = self.request.query_params.get('projet')
    if projet_id:
      queryset = queryset.filter(projet_id=projet_id)
    return queryset

class TacheRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = TacheSerializers
  permission_classes = [IsAuthenticated]
  lookup_field = 'id'

  def get_queryset(self):
    return Tache.objects.filter(projet__user=self.request.user)

class SousTacheListCreateView(generics.ListCreateAPIView):
  serializer_class = SousTacheSerializers
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    queryset = Sous_Tache.objects.filter(tache__projet__user=self.request.user)
    tache_id = self.request.query_params.get('tache')
    if tache_id:
      queryset = queryset.filter(tache_id=tache_id)
    return queryset

class SousTacheRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = SousTacheSerializers
  permission_classes = [IsAuthenticated]
  lookup_field = 'id'

  def get_queryset(self):
    return Sous_Tache.objects.filter(tache__projet__user=self.request.user)