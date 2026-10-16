from django.contrib import admin
from .models import *

admin.site.register([Projet, Tache, Sous_Tache])
