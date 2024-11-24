from .models import InventoryItem, Category
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class InventoryItemViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create category for inventory items
        self.category = Category.objects.create(name='Electronics', description='Devices')
        
        self.inventory_item_data = {
            'name': 'Laptop',
            'category': self.category.id,
            'quantity': 50,
            'unit_price': 50000.00,
            'description': 'High-performance laptop'
        }

    def test_create_inventory_item(self):
        response = self.client.post('/api/inventory/', self.inventory_item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.inventory_item_data['name'])
        self.assertEqual(response.data['quantity'], self.inventory_item_data['quantity'])

    def test_get_inventory_items(self):
        InventoryItem.objects.create(
            name='Laptop',
            category=self.category,
            quantity=10,
            unit_price=40000.00,
            description='Gaming laptop'
        )
        response = self.client.get('/api/inventory/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_inventory_item_by_id(self):
        item = InventoryItem.objects.create(
            name='Tablet',
            category=self.category,
            quantity=25,
            unit_price=20000.00,
            description='Portable tablet'
        )
        response = self.client.get(f'/api/inventory/{item.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], item.name)

    def test_update_inventory_item(self):
        item = InventoryItem.objects.create(
            name='Smartphone',
            category=self.category,
            quantity=30,
            unit_price=25000.00,
            description='Smartphone with great features'
        )
        updated_data = {
            'name': 'Smartphone Pro',
            'category': self.category.id,
            'quantity': 35,
            'unit_price': 30000.00,
            'description': 'Upgraded smartphone with new features'
        }
        response = self.client.put(f'/api/inventory/{item.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_data['name'])

    def test_delete_inventory_item(self):
        item = InventoryItem.objects.create(
            name='Smartwatch',
            category=self.category,
            quantity=20,
            unit_price=10000.00,
            description='Wearable smartwatch'
        )
        response = self.client.delete(f'/api/inventory/{item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
