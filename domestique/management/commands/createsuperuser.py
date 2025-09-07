from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from domestique.models import Utilisateur
from django.utils.translation import gettext_lazy as _

class Command(BaseCommand):
    help = 'Crée un superutilisateur pour l\'application Copal'

    def handle(self, *args, **options):
        self.stdout.write("Création d'un superutilisateur pour Copal")
        
        # Demander les informations
        nom = input("Nom : ")
        prenom = input("Prénom : ")
        email = input("Email : ")
        mot_de_passe = input("Mot de passe : ")
        telephone = input("Téléphone : ")

        # Vérifier si l'email existe déjà
        if Utilisateur.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR("Erreur : Cet email existe déjà."))
            return

        # Créer le superutilisateur
        utilisateur = Utilisateur(
            nom=nom,
            prenom=prenom,
            email=email,
            mot_de_passe=make_password(mot_de_passe),
            telephone=telephone,
            est_admin=True,
            est_client=False,
            est_prestataire=False,
            suppression_logique=False
        )
        utilisateur.save()

        self.stdout.write(self.style.SUCCESS(f"Superutilisateur {email} créé avec succès !"))