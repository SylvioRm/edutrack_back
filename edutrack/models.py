from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Projet(models.Model):
  titre = models.CharField(max_length=150)
  description = models.TextField(blank=True, null=True)
  date_debut = models.DateField()
  date_fin = models.DateField()
  progression = models.IntegerField(default=0)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def clean(self):
    super().clean()
    if self.date_debut and self.date_fin and self.date_debut > self.date_fin:
      raise ValidationError(
          {'date_fin': 'La date de fin ne peut pas être antérieure à la date de début.'}
      )

  def save(self, *args, **kwargs):
    self.full_clean()
    super().save(*args, **kwargs)

  def calculer_et_mettre_a_jour_progression(self):
    taches = self.tache_set.all()
    if not taches.exists():
      self.progression = 0
      Projet.objects.filter(pk=self.pk).update(progression=0)
      return

    total_elements = 0
    elements_termines = 0

    for tache in taches:
      sous_taches = tache.sous_tache_set.all()
      if sous_taches.exists():
        for st in sous_taches:
          total_elements += 1
          if st.status.lower() in ['termine', 'terminé']:
            elements_termines += 1
      else:
        total_elements += 1
        if tache.status.lower() in ['termine', 'terminé']:
          elements_termines += 1

    if total_elements > 0:
      self.progression = int((elements_termines / total_elements) * 100)
    else:
      self.progression = 0

    Projet.objects.filter(pk=self.pk).update(progression=self.progression)

  def __str__(self):
    return f'{self.titre} : {self.date_debut} - {self.date_fin}'


class Tache(models.Model):
  titre = models.CharField(max_length=150)
  description = models.TextField(blank=True, null=True)
  status = models.CharField(max_length=50, default='en_cours')
  projet = models.ForeignKey(Projet, on_delete=models.CASCADE)

  def verifier_et_mettre_a_jour_statut(self):
    if not self.pk:
      return

    sous_taches = self.sous_tache_set.all()
    if sous_taches.exists():
      toutes_terminees = all(
          st.status.lower() in ['termine', 'terminé'] for st in sous_taches
      )
      if toutes_terminees:
        self.status = 'termine'
      else:
        self.status = 'en_cours'

  def save(self, *args, **kwargs):
    self.verifier_et_mettre_a_jour_statut()

    super().save(*args, **kwargs)

    self.projet.calculer_et_mettre_a_jour_progression()

  def delete(self, *args, **kwargs):
    projet = self.projet
    super().delete(*args, **kwargs)
    projet.calculer_et_mettre_a_jour_progression()

  def __str__(self):
    return f'{self.titre} : {self.status}'

class Sous_Tache(models.Model):
  titre = models.CharField(max_length=150)
  status = models.CharField(max_length=50, default='en_cours')
  tache = models.ForeignKey(Tache, on_delete=models.CASCADE)

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    
    self.tache.verifier_et_mettre_a_jour_statut()
    Tache.objects.filter(pk=self.tache.pk).update(status=self.tache.status)

    self.tache.projet.calculer_et_mettre_a_jour_progression()

  def delete(self, *args, **kwargs):
    tache = self.tache
    super().delete(*args, **kwargs)
    
    tache.verifier_et_mettre_a_jour_statut()
    Tache.objects.filter(pk=tache.pk).update(status=tache.status)
    tache.projet.calculer_et_mettre_a_jour_progression()

  def __str__(self):
    return f'{self.titre} : {self.status}'