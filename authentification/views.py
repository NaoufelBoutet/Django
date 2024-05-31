from django.shortcuts import render,redirect
from django.contrib.auth import login, logout,authenticate,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from authentification.models import UserProfile
import datetime





def connexion(request):
    message = ""
    if request.method == "POST":
        username = request.POST["username"]
        motdepasse = request.POST["motdepasse"]
        verification = authenticate(username = username,
                                    password = motdepasse)
        if verification != None:
            login(request,verification) 
            return redirect("index")
        else:
            message = "username et/ou mot de passe incorrect"
    return render(request,"connexion.html", context = {"message":message})

def deconnexion(request):
    logout(request)
    return redirect("index")





def inscription(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        city = request.POST['city']
        birth_day = request.POST['birth_day']
        
        try:
            birth_day =  datetime.datetime.strptime(birth_day, '%Y-%m-%d').date()
        
        except ValueError:
            error_message = "Le format de la date de naissance n'est pas valide. Utilisez le format AAAA-MM-JJ."
            return render(request, 'inscription.html', {'error_message': error_message})
        if password1 == password2:
            if not User.objects.filter(username=username).exists():
                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(
                        username=username,
                        password=password1,
                        email=email,
                        first_name=first_name,
                        last_name=last_name
                        
                    )
                    
        
                    # Créer un profil UserProfile associé à l'utilisateur
                    profile = UserProfile.objects.create(
                            user=user,
                            city=city,
                            birth_day=birth_day
                            
                    )
                    
                    user = authenticate(username=username, password=password1)
                    return redirect('connexion')
                else:
                    error_message = "L'email est déjà utilisé"
            else:
                error_message = "Le nom d'utilisateur est déjà pris"
        else:
            error_message = "Les mots de passe ne correspondent pas"
        
        return render(request, 'inscription.html', {'error_message': error_message})
    return render(request, 'inscription.html')
    
    

def home(request):
    return render(request, 'index.html')






