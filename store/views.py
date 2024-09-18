from datetime import timezone
from multiprocessing.connection import Client
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as auth_login ,logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Reservation, Vehicule
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful")
            return redirect('dashboard')  # Redirect to home page
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        # Extract form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Create user manually
        if password1 == password2:
            try:
                user = User.objects.create_user(
                    username=email,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password1
                )
                user.save()
                messages.success(request, "Registration successful. Please log in.")
                return redirect('login')  # Redirect to the login page after registration
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, "Passwords do not match")

    return render(request, 'register.html')


def logout_view(request):
    """Log out the user and redirect to the home page."""
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')  # Redirect to home page or any other page


@login_required
def profile_view(request):
    """Render the user's profile page."""
    return render(request, 'profile.html', {'user': request.user})

@login_required
def home_view(request):
    return render(request, 'home.html')

def dashboard(request):
    vehicules = Vehicule.objects.all()
    # You can add context data here if needed
    return render(request, 'dashboard.html')

@login_required
def add_vehicule(request):
    if request.method == 'POST':
        marque = request.POST.get('marque')
        modele = request.POST.get('modele')
        annee = request.POST.get('annee')
        couleur = request.POST.get('couleur')
        type_carburant = request.POST.get('type_carburant')
        capacite = request.POST.get('capacite')
        prix_par_jour = request.POST.get('prix_par_jour')
        immatriculation = request.POST.get('immatriculation')
        kilometrage = request.POST.get('kilometrage')
        etat = request.POST.get('etat')
    
        
        # Validation could be added here if needed
        
        # Create and save the new Vehicule instance
        vehicule = Vehicule(
            marque=marque,
            modele=modele,
            annee=annee,
            couleur=couleur,
            type_carburant=type_carburant,
            capacite=capacite,
            prix_par_jour=prix_par_jour,
            immatriculation=immatriculation,
            kilometrage=kilometrage,
            etat=etat,
       
        )
        vehicule.save()
        
        messages.success(request, "Véhicule ajouté avec succès !")
        return redirect('add_vehicule')  # Redirect after success
        
    return render(request, 'add_vehicule.html')



def list_vehicules(request):
    vehicules = Vehicule.objects.all()
    return render(request, 'list_vehicules.html', {'vehicules': vehicules})


@login_required
def update_vehicule(request, id):
    vehicule = get_object_or_404(Vehicule, id=id)

    # List of possible 'etat' values
    etat_list = ['disponible', 'réservé', 'maintenance']

    if request.method == 'POST':
        marque = request.POST.get('marque')
        modele = request.POST.get('modele')
        annee = request.POST.get('annee')
        couleur = request.POST.get('couleur')
        type_carburant = request.POST.get('type_carburant')
        capacite = request.POST.get('capacite')
        prix_par_jour = request.POST.get('prix_par_jour')
        immatriculation = request.POST.get('immatriculation')
        kilometrage = request.POST.get('kilometrage')
        etat = request.POST.get('etat')

        if request.FILES.get('photo'):
            vehicule.photo = request.FILES.get('photo')

        vehicule.marque = marque
        vehicule.modele = modele
        vehicule.annee = annee
        vehicule.couleur = couleur
        vehicule.type_carburant = type_carburant
        vehicule.capacite = capacite
        vehicule.prix_par_jour = prix_par_jour
        vehicule.immatriculation = immatriculation
        vehicule.kilometrage = kilometrage
        vehicule.etat = etat

        vehicule.save()
        messages.success(request, "Véhicule mis à jour avec succès !")
        return redirect('list_vehicules')

    return render(request, 'update_vehicule.html', {'vehicule': vehicule, 'etat_list': etat_list})


@login_required
def delete_vehicule(request, id):
    vehicule = get_object_or_404(Vehicule, id=id)
    if request.method == 'POST':
        vehicule.delete()
        messages.success(request, "Véhicule supprimé avec succès !")
        return redirect('list_vehicules')
    return redirect('list_vehicules')  # Redirect if not a POST request (e.g., direct access)








######## client ##############

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Client

from django.db import IntegrityError

@login_required
def list_clients(request):
    clients = Client.objects.filter(user=request.user)
    return render(request, 'list_clients.html', {'clients': clients})




from django.utils import timezone

@login_required
def add_client(request):
    if request.method == 'POST':
        # Collect data from the request
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        adresse = request.POST.get('adresse')
        permis_conduire = request.FILES.get('permis_conduire')

        # Validate required fields
        if not nom or not prenom or not email:
            messages.error(request, 'Nom, prénom, and email are required fields.')
        else:
            # Create and save the new Client instance
            try:
                client = Client.objects.create(
                    user=request.user,
                    nom=nom,
                    prenom=prenom,
                    email=email,
                    telephone=telephone,
                    adresse=adresse,
                    permis_conduire=permis_conduire,
                    date_inscription=timezone.now()
                )
                messages.success(request, 'Client added successfully!')
                return redirect('list_clients')
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

    return render(request, 'add_client.html')


@login_required
def update_client(request, id):
    client = get_object_or_404(Client, id=id)
    
    if request.method == 'POST':
        # Collect data from the request
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        adresse = request.POST.get('adresse')
        permis_conduire = request.FILES.get('permis_conduire')
        
        # Update the Client instance
        client.nom = nom
        client.prenom = prenom
        client.email = email
        client.telephone = telephone
        client.adresse = adresse
        
        # Handle file upload
        if permis_conduire:
            client.permis_conduire = permis_conduire
        
        client.save()
        messages.success(request, 'Client updated successfully!')
        return redirect('list_clients')

    return render(request, 'update_client.html', {'client': client})



@login_required
def delete_client(request, id):
    client = get_object_or_404(Client, id=id)
    client.delete()
    messages.success(request, 'Client deleted successfully!')
    return redirect('list_clients')




##############


def reserved_vehicles_list(request):
    # Retrieve all reservations where the status is 'confirmée'
    reservations = Reservation.objects.filter(statut='confirmée')
    return render(request, 'reserved_vehicles_list.html', {'reservations': reservations})