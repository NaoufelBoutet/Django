import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_logout_view(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    response = client.get('/deconnexion')
    assert response.status_code == 302  # Redirection après la déconnexion
    assert response.url == "/"          # Redirection vers la page d'accueil


@pytest.mark.django_db
def test_successful_registration(client):
    response = client.post(reverse('inscription'), {
        'username': 'testuser',
        'password1': 'testpassword',
        'password2': 'testpassword',
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'city': 'Test City',
        'birth_day': '2000-01-01',
    })
    assert response.status_code == 302  # Redirection après l'inscription
    assert response.url == reverse('connexion')  # Redirection vers la page de connexion




@pytest.mark.django_db
def test_registration_with_existing_username(client):
    # Créer un utilisateur existant
    User.objects.create_user(username='testuser', password='testpassword')
    
    response = client.post(reverse('inscription'), {
        'username': 'testuser',  # Utiliser le même nom d'utilisateur
        'password1': 'testpassword',
        'password2': 'testpassword',
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'city': 'Test City',
        'birth_day': '2000-01-01',
    })
    assert response.status_code == 200  # Reste sur la même page d'inscription
    assert "Inscription" in response.content.decode()

@pytest.mark.django_db
def test_successful_login(client):
    # Créer un utilisateur pour le test
    user = User.objects.create_user(username='testuser', password='testpassword')
    
    response = client.post(reverse('connexion'), {'username': 'testuser', 'motdepasse': 'testpassword'})
    assert response.status_code == 302  # Redirection après la connexion
    assert response.url == reverse('index')  # Redirection vers la page d'accueil
    assert '_auth_user_id' in client.session  # Vérifier que l'utilisateur est connecté



@pytest.mark.django_db
def test_login_with_incorrect_credentials(client):
    response = client.post(reverse('connexion'), {'username': 'wronguser', 'motdepasse': 'wrongpassword'})
    assert response.status_code == 200  # Reste sur la même page de connexion
    assert 'username et/ou mot de passe incorrect' in response.content.decode()

@pytest.mark.django_db
def test_successful_logout(client):
    # Créer un utilisateur et le connecter pour le test
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.login(username='testuser', password='testpassword')
    
    response = client.get(reverse('deconnexion'))
    assert response.status_code == 302  # Redirection après la déconnexion
    assert response.url == reverse('index')  # Redirection vers la page d'accueil
    assert '_auth_user_id' not in client.session  # Vérifier que l'utilisateur est déconnecté