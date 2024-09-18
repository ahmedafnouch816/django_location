from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
# Create your models here.


class Vehicule(models.Model):
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    annee = models.IntegerField()
    couleur = models.CharField(max_length=50)
    type_carburant = models.CharField(max_length=50)
    capacite = models.IntegerField()
    prix_par_jour = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    #photo = models.ImageField(upload_to='vehicules/')  # Ensure this line exists
    immatriculation = models.CharField(max_length=50, unique=True)
    kilometrage = models.IntegerField()
    etat = models.CharField(max_length=50, choices=[('disponible', 'Disponible'), ('reservé', 'Réservé'), ('maintenance', 'Maintenance')])

    def __str__(self):
        return f"{self.marque} {self.modele}"
class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()  # Removed unique=True to allow duplicate emails
    telephone = models.CharField(max_length=15, null=True, blank=True)
    adresse = models.TextField(null=True, blank=True)
    permis_conduire = models.FileField(upload_to='permis/', null=True, blank=True)
    date_inscription = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Reservation(models.Model):
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)  # Lien vers le véhicule réservé
    client = models.ForeignKey(Client, on_delete=models.CASCADE)      # Lien vers le client ayant fait la réservation
    date_debut = models.DateTimeField()                                # Date et heure de début de la réservation
    date_fin = models.DateTimeField()                                  # Date et heure de fin de la réservation
    prix_total = models.DecimalField(max_digits=10, decimal_places=2) # Prix total de la réservation
    statut = models.CharField(max_length=20, choices=[('en_attente', 'En attente'), ('confirmée', 'Confirmée'), ('annulée', 'Annulée')])  # Statut de la réservation
    date_reservation = models.DateTimeField(auto_now_add=True)         # Date à laquelle la réservation a été effectuée

    def __str__(self):
        return f"Réservation {self.id} - {self.client} pour {self.vehicule}"

    def save(self, *args, **kwargs):
        # Calcul du prix total en fonction du nombre de jours
        if self.date_debut and self.date_fin:
            delta = self.date_fin - self.date_debut
            self.prix_total = delta.days * self.vehicule.prix_par_jour
        super().save(*args, **kwargs)


class Paiement(models.Model):
    reservation = models.ForeignKey('Reservation', on_delete=models.CASCADE, related_name='paiements')  # Lien vers la réservation associée
    montant = models.DecimalField(max_digits=10, decimal_places=2)  # Montant payé
    date_paiement = models.DateTimeField(auto_now_add=True)           # Date et heure du paiement
    mode_paiement = models.CharField(max_length=20, choices=[('carte', 'Carte de crédit'), ('virement', 'Virement bancaire'), ('espèce', 'Espèce')])  # Mode de paiement

    def __str__(self):
        return f"Paiement {self.id} pour Réservation {self.reservation.id} - {self.montant} {self.mode_paiement}"
    
    
    
    
    
class ContratLocation(models.Model):
    reservation = models.OneToOneField('Reservation', on_delete=models.CASCADE, related_name='contrat')  # Lien vers la réservation associée
    date_signature = models.DateTimeField(auto_now_add=True)  # Date à laquelle le contrat a été signé
    conditions = models.TextField()                          # Conditions spécifiques du contrat

    def __str__(self):
        return f"Contrat {self.id} pour Réservation {self.reservation.id} signé le {self.date_signature}"
    
    
    
class HistoriqueVehicule(models.Model):
    vehicule = models.ForeignKey('Vehicule', on_delete=models.CASCADE, related_name='historique')  # Lien vers le véhicule concerné
    date_evenement = models.DateTimeField()  # Date de l'événement
    type_evenement = models.CharField(max_length=50, choices=[('entretien', 'Entretien'), ('réparation', 'Réparation'), ('incident', 'Incident')])  # Type d'événement
    description = models.TextField()         # Description de l'événement

    def __str__(self):
        return f"Événement {self.type_evenement} pour Véhicule {self.vehicule.id} le {self.date_evenement}"