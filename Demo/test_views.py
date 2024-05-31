import pytest
from django.test import Client
from django.contrib.auth.models import User

@pytest.fixture
def client():
    return Client()


@pytest.mark.django_db
def test_index_view():
    client = Client()
    response = client.get('/')
    assert response.status_code == 200
    assert 'Bienvenue chez PrédiSchool !!' in response.content.decode()

@pytest.mark.django_db
def test_architechture_view():
    client = Client()
    user = User.objects.create_user(username='testuser', password='12345')
    client.force_login(user)
    response = client.get('/architechture')
    assert response.status_code == 200
    assert "Vous pouvez aussi choisir de nous déposer un document pour l'analyser!!" in response.content.decode()

@pytest.mark.django_db
def test_profile_view():
    client = Client()
    user = User.objects.create_user(username='testuser', password='12345')
    client.force_login(user)
    response = client.get('/profile')
    assert response.status_code == 200
    assert "Vos informations utilisateur !" in response.content.decode()