from .models import InventoryItem
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class StockAdjustmentViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        
        # Create an inventory item for testing stock adjustment
        self.item = InventoryItem.objects.create(
            name='Camera',
            category=self.category,
            quantity=100,
            unit_price=30000.00,
            description='DSLR Camera'
        )

    def test_stock_adjustment(self):
        data = {
            'item_id': self.item.id,
            'quantity': 120
        }
        response = self.client.post('/api/stock-adjustment/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 120)

    def test_invalid_quantity_stock_adjustment(self):
        data = {
            'item_id': self.item.id,
            'quantity': 'invalid'
        }
        response = self.client.post('/api/stock-adjustment/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_item_id_or_quantity(self):
        data = {'quantity': 150}
        response = self.client.post('/api/stock-adjustment/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_low_stock_items(self):
        low_stock_item = InventoryItem.objects.create(
            name='Headphones',
            category=self.category,
            quantity=5,
            unit_price=2000.00,
            description='Wireless headphones'
        )
        response = self.client.get('/api/stock-adjustment/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['low_stock_items']), 0)
