from django.contrib import admin

from .models import Vehicule, Client, Reservation, Paiement,ContratLocation,HistoriqueVehicule

# Register your models here.

admin.site.register(Vehicule)
admin.site.register(Client)
admin.site.register(Reservation)
admin.site.register(Paiement)
admin.site.register(ContratLocation)
admin.site.register(HistoriqueVehicule)