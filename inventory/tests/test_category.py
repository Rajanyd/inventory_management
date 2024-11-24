from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category
from django.contrib.auth.models import User

class CategoryViewTests(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.category_data = {'name': 'Electronics', 'description': 'Devices and gadgets'}

    def test_create_category(self):
        response = self.client.post('/api/categories/', self.category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.category_data['name'])
        self.assertEqual(response.data['description'], self.category_data['description'])

    def test_get_all_categories(self):
        Category.objects.create(name='Electronics', description='Devices')
        Category.objects.create(name='Furniture', description='Home furniture')
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_category_by_id(self):
        category = Category.objects.create(name='Books', description='Reading material')
        response = self.client.get(f'/api/categories/{category.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], category.name)

    def test_update_category(self):
        category = Category.objects.create(name='Toys', description='Play items')
        updated_data = {'name': 'Toys & Games', 'description': 'Play and gaming items'}
        response = self.client.put(f'/api/categories/{category.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_data['name'])
        self.assertEqual(response.data['description'], updated_data['description'])

    def test_delete_category(self):
        category = Category.objects.create(name='Clothing', description='Apparel')
        response = self.client.delete(f'/api/categories/{category.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
