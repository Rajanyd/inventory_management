from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mongoengine.errors import DoesNotExist
from .models import Category, InventoryItem, StockAdjustment
from .serializers import CategorySerializer, InventoryItemSerializer, StockAdjustmentSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login,logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.generic import TemplateView
from mongoengine.errors import ValidationError
from django.shortcuts import render, redirect
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from .utils.sns_notifications import send_low_stock_alert



class CategoryView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all categories",
        responses={200: CategorySerializer(many=True)}
    )
    def get(self, request):
        print(f"User: {request.user}")  
        if request.user.is_authenticated:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data)
        return Response({"detail": "Authentication failed"}, status=401)
    
    @swagger_auto_schema(
        operation_description="Create a new category",
        request_body=CategorySerializer,
        responses={201: CategorySerializer, 400: "Bad Request"}
    )

    def post(self, request):
        try:
            serializer = CategorySerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error creating category: {e}")
            return Response({"error": "An error occurred while creating the category."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            category = Category.objects.get(id=pk)
        except DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            category = Category.objects.get(id=pk)
        except DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            category = Category.objects.get(id=pk)
        except DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

        category.delete()
        return Response({"message": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class InventoryItemView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all inventory items",
        responses={200: InventoryItemSerializer(many=True)}
    )
    def get(self, request):
        print(f"User: {request.user}")  # Log the authenticated user
        if request.user.is_authenticated:
            categories = InventoryItem.objects.all()
            serializer = InventoryItemSerializer(categories, many=True)
            return Response(serializer.data)
        return Response({"detail": "Authentication failed"}, status=401)
    

    @swagger_auto_schema(
        operation_description="Create a new inventory item",
        request_body=InventoryItemSerializer,
        responses={201: InventoryItemSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        print("Received data:", request.data)  # Add this line to inspect the incoming data
        serializer = InventoryItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InventoryItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            item = InventoryItem.objects.get(pk=pk)
        except DoesNotExist:
            return Response({"error": "Inventory item not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = InventoryItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            item = InventoryItem.objects.get(pk=pk)
        except DoesNotExist:
            return Response({"error": "Inventory item not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = InventoryItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            item = InventoryItem.objects.get(pk=pk)
        except DoesNotExist:
            return Response({"error": "Inventory item not found."}, status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response({"message": "Inventory item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class StockAdjustmentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Adjust stock for an inventory item",
        request_body=StockAdjustmentSerializer,
        responses={200: StockAdjustmentSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        """
        Adjust stock levels by setting a new quantity directly.
        """
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        item_id = data.get("item_id")
        new_quantity = data.get("quantity")

        # Validate inputs
        if item_id is None or new_quantity is None:
            return Response({"error": "Item ID and quantity are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the inventory item
        item = get_object_or_404(InventoryItem, id=item_id)

        # Update stock to the new quantity
        try:
            new_quantity = int(new_quantity)
        except ValueError:
            return Response({"error": "Quantity must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)

        item.quantity = new_quantity
        item.save()

        # Check if stock is below the threshold and send notification if necessary
        LOW_STOCK_THRESHOLD = 10
        if item.quantity < LOW_STOCK_THRESHOLD:
            send_low_stock_alert(item.name, item.quantity, LOW_STOCK_THRESHOLD, user.email)

        return Response(
            {
                "message": f"Stock for item '{item.name}' updated successfully.",
                "item": InventoryItemSerializer(item).data,
            },
            status=status.HTTP_200_OK,
        )
    @swagger_auto_schema(
        operation_description="Retrieve all low stock items below the defined threshold",
        responses={200: InventoryItemSerializer(many=True)}
    )
    def get(self, request):
        """
        Fetch all low-stock items below a defined threshold.
        """
        LOW_STOCK_THRESHOLD = 10
        low_stock_items = InventoryItem.objects.filter(quantity__lt=LOW_STOCK_THRESHOLD)
        serializer = InventoryItemSerializer(low_stock_items, many=True)
        return Response(
            {
                "message": f"Items below the stock threshold ({LOW_STOCK_THRESHOLD}):",
                "low_stock_items": serializer.data,
            },
            status=status.HTTP_200_OK,
        )



class StockAdjustmentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        adjustment = get_object_or_404(StockAdjustment, pk=pk)
        serializer = StockAdjustmentSerializer(adjustment)
        return Response(serializer.data)

    def put(self, request, pk):
        adjustment = get_object_or_404(StockAdjustment, pk=pk)
        serializer = StockAdjustmentSerializer(adjustment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        adjustment = get_object_or_404(InventoryItem, pk=pk)
        adjustment.delete()
        return Response({"message": "Stock adjustment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate using the custom user model
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Generate JWT tokens for the user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Set cookies securely for both access and refresh tokens
            response = redirect('dashboard')  # Redirect after successful login
            response.set_cookie('access_token', access_token, httponly=True, secure=True)  # Secure cookies for production
            response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True)  # Secure cookies for production

            return response
        else:
            # Invalid credentials handling
            return render(request, 'inventory/login.html', {'error': 'Invalid credentials'})

    return render(request, 'inventory/login.html')

def logout_view(request):
    # Remove JWT tokens from cookies
    response = redirect('login')  # Redirect to login page after logout
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    
    # Logout the user
    logout(request)

    return response


def dashboard_view(request):
    return render(request, 'inventory/dashboard.html')


# Example views for list of categories and inventory items (may use API calls from the frontend)
class CategoryListView(TemplateView):
    template_name = 'inventory/category_list.html'


class InventoryItemListView(TemplateView):
    template_name = 'inventory/inventory_item_list.html'


class StockAdjustmentListView(TemplateView):
    template_name = 'inventory/stock_adjustment_list.html'


class CreateCategoryView(TemplateView):
    template_name = 'inventory/create_category.html'

class CreateInventoryView(TemplateView):
    template_name = 'inventory/create_inventory_item.html'

class StockAdjustmentView(TemplateView):
    template_name = 'inventory/stock_adjustment.html'


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories_count = Category.objects.count()
        inventory_items_count = InventoryItem.objects.count()
        stock_adjustments_count = StockAdjustment.objects.count()
        
        low_stock_items = InventoryItem.objects.filter(quantity__lt=10).count()  # Example threshold

        return Response({
            'categories': categories_count,
            'inventoryItems': inventory_items_count,
            'stockAdjustments': stock_adjustments_count,
            'lowStockItems': low_stock_items
        })
