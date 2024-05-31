import pytest
from authentification.models import UserProfile
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_my_model_creation():
    # Crée un utilisateur pour fournir un user_id valide
    user = User.objects.create(username='testuser')

    # Crée un objet UserProfile avec les champs requis, y compris user_id
    UserProfile.objects.create(user_id=user.id, birth_day='1958-11-23', city='Description for testing')

    assert UserProfile.objects.count() == 1