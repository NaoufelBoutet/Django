import pytest
from django.contrib.auth.models import User

@pytest.fixture
def super_user():
    return User.objects.create_superuser(username='admin', email='admin@example.com', password='password')