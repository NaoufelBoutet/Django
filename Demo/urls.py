"""
URL configuration for Demo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from application import views
from authentification import views as con_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name = "index"),
    path('prediction',views.prediction, name = "prediction"),
    path('connexion',con_views.connexion, name = "connexion"),
    path('deconnexion',con_views.deconnexion, name = "deconnexion"),
    path('inscription',con_views.inscription, name = "inscription"),
    path('monitoring',views.ma_vue_protegee_super_utilisateur, name = "Monitoring"),
    path('profile',views.profile, name = "profile")
]
