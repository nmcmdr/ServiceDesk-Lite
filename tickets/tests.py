import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Ticket
from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user(db):
    user = User.objects.create_user(username='testuser', password='password123', email='test@example.com')
    return user


@pytest.fixture
def test_admin(db):
    admin = User.objects.create_user(
        username='adminuser',
        password='password123',
        email='admin@example.com',
        role=User.ROLE_ADMIN,
        is_staff=True
    )
    return admin


@pytest.fixture
def test_ticket(db, test_user):
    return Ticket.objects.create(title="Test Ticket", description="A test description.", author=test_user)


@pytest.mark.django_db
class TestTicketAPI:

    def test_create_ticket_authenticated(self, api_client, test_user):
        api_client.force_authenticate(user=test_user)
        url = reverse('ticket-list')
        data = {'title': 'New Ticket', 'description': 'Need help!'}

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Ticket.objects.count() == 1
        assert Ticket.objects.get().title == 'New Ticket'

    def test_create_ticket_unauthenticated(self, api_client):
        url = reverse('ticket-list')
        data = {'title': 'Should Fail', 'description': 'This should not be created.'}

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_ticket_by_owner(self, api_client, test_user, test_ticket):
        api_client.force_authenticate(user=test_user)
        url = reverse('ticket-detail', kwargs={'pk': test_ticket.pk})

        # Act
        response = api_client.delete(url)

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Ticket.objects.filter(pk=test_ticket.pk).exists()

    def test_delete_ticket_by_admin(self, api_client, test_admin, test_ticket):
        api_client.force_authenticate(user=test_admin)
        url = reverse('ticket-detail', kwargs={'pk': test_ticket.pk})

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Ticket.objects.filter(pk=test_ticket.pk).exists()

    def test_delete_ticket_by_other_user_fails(self, api_client, db, test_ticket):
        other_user = User.objects.create_user(username='otheruser', password='password123')
        api_client.force_authenticate(user=other_user)
        url = reverse('ticket-detail', kwargs={'pk': test_ticket.pk})

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN  # 403 Forbidden - нет прав
        assert Ticket.objects.filter(pk=test_ticket.pk).exists()