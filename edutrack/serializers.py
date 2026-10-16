from .models import *
from rest_framework import serializers

class ProjetSerializers(serializers.ModelSerializer):
    class Meta:
        model = Projet
        fields = '__all__'
        read_only_fields = ['id', 'user', 'progression']

class TacheSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tache
        fields = '__all__'
        read_only_fields = ['id']

class SousTacheSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sous_Tache
        fields = '__all__'
        read_only_fields = ['id']
