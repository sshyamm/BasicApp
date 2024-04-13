from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Coin

class CoinAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.coin1 = Coin.objects.create(
            coin_name='Test Coin 1',
            coin_desc='Description of Test Coin 1',
            coin_year=2022,
            coin_country='Test Country',
            coin_material='Test Material',
            coin_weight=10.5,
            starting_bid=100.0,
            coin_status='available'
        )

    def test_list_coins(self):
        url = reverse('coin-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_coin(self):
        url = reverse('coin-detail', kwargs={'pk': self.coin1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_coin(self):
        url = reverse('coin-detail', kwargs={'pk': self.coin1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_coin(self):
        url = reverse('coin-list')
        data = {
            'coin_name': 'New Test Coin',
            'coin_desc': 'Description of New Test Coin',
            'coin_year': 2023,
            'coin_country': 'New Test Country',
            'coin_material': 'New Test Material',
            'coin_weight': 15.0,
            'starting_bid': 150.0,
            'coin_status': 'available'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_coin(self):
        url = reverse('coin-detail', kwargs={'pk': self.coin1.pk})
        data = {
            'coin_name': 'Updated Test Coin',
            'coin_desc': 'Updated Description of Test Coin 1',
            'coin_year': 2023,
            'coin_country': 'Updated Test Country',
            'coin_material': 'Updated Test Material',
            'coin_weight': 15.0,
            'starting_bid': 150.0,
            'coin_status': 'available'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
