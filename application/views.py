from django.shortcuts import render
from django.contrib.auth.decorators import login_required,user_passes_test
from pymongo import MongoClient
import re
import os
from authentification.models import UserProfile
# Connexion à la base de données MongoDB
client = MongoClient("mongodb://mongoadmin:GRETA2024@vm-kaelig-mooc.francecentral.cloudapp.azure.com")
print("CLIENT",client)
db = client.Mooc
students_collection = db.message_par_user

def nombre_reussi():
    pipeline = [
        {
            "$project": {
                "notes": {
                    "$objectToArray": "$notes"
                }
            }
        },
        {
            "$unwind": "$notes"
        },
        {
            "$match": { "notes.v.certif": "Y" }
        },
        {
            "$group": {
                "_id": "$notes.k",
                "validatedCount": { "$sum": 1 }
            }
        },
        {
            "$sort": { "validatedCount": -1 }
        }
    ]

    result = students_collection.aggregate(pipeline)

    liste = []
    for element in result:
        element["id"] = re.split(r'[+/\\:]' , str(element["_id"]))  
        del element["_id"]
        liste.append(element)
    return liste

def Moyenne():
    pipeline = [
    {
        "$project": {
            "notes": {
                "$objectToArray": "$notes"
            }
        }
    },
    {
        "$unwind": "$notes"
    },
    {
        "$match": {
            "$and": [
                { "notes.v.note": { "$ne": "null" } },
                { "notes.v.note": { "$ne": "" } },
                { "notes.v.note": { "$type": "string" } }
            ]
        }
    },
    {
        "$group": {
            "_id": "$notes.k",
            "averageScore": { "$avg": { "$toDouble": "$notes.v.note" } }
        }
    },
    {
        "$project": {
            "_id": 1,
            "averageScore": { "$round": ["$averageScore", 3] } # Arrondir au deuxième chiffre
        }
    }
]

    result = students_collection.aggregate(pipeline)
    liste = []
    for element in result:
        element["id"] = re.split(r'[+/\\:]' , str(element["_id"]))
        del element["_id"]
        liste.append(element)
    return liste
   



def index(request):
    dico_url = {"CNAM01002":"https://dz03nossv7tsm.cloudfront.net/media/filer_public_thumbnails/filer_public/65/14/65149675-ff7a-42f2-85f6-573dac1b781c/fun_c-dejoux_du-manager.jpg__300x170_q85_crop-smart_subsampling-2_upscale.jpg",
                }
    liste_reussite = nombre_reussi()
    liste_moyenne = Moyenne()
    liste_affichage = []
    
    moyennes_dict = {tuple(moyenne['id']): moyenne['averageScore'] for moyenne in liste_moyenne}

    for element in liste_reussite:
        dico_affichage = {}
        id_tuple = tuple(element["id"])
        dico_affichage["id"] = element["id"]
        dico_affichage["id"][1]= dico_affichage["id"][1].split("S")[0]
        dico_affichage["validatedCount"] = element["validatedCount"]
        
        dico_affichage["averageScore"] = moyennes_dict.get(id_tuple, 0.0)  

        liste_affichage.append(dico_affichage)
    
    return render(request, "index.html", context={"liste_affichage": liste_affichage})
@login_required
def architechture(request):
    if request.method == "POST":
        message = request.POST.get("message", "")
        if message:
            return render(request, "architechture.html", {"message": message})
        else:
            message_error = "Rentrez un message pour lancer la prédiction!"
            return render(request, "architechture.html", {"message_error": message_error})
    
    # Si la requête n'est pas de type POST, renvoyer simplement la page sans message
    return render(request, "architechture.html")



def est_super_utilisateur(user):
    return user.is_superuser

@user_passes_test(est_super_utilisateur)
def ma_vue_protegee_super_utilisateur(request):
    
    return render(request, 'monitoring.html')


def profile(request):
    user = request.user  # Récupérer l'utilisateur connecté
    try:
        profile = UserProfile.objects.get(user=user)  # Récupérer le profil utilisateur associé
    except UserProfile.DoesNotExist:
        profile = None  # Gérer le cas où le profil n'existe pas

    context = {"username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "city": profile.city if profile else None,
            "birth_day": profile.birth_day if profile else None,
            }
    return render(request, "profile.html", context)
    
            
    