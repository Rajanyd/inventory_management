from rest_framework import serializers
from .models import Category, InventoryItem, StockAdjustment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class InventoryItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())  # or use a StringRelatedField if needed

    class Meta:
        model = InventoryItem
        fields = ['id','name', 'category', 'quantity', 'unit_price', 'description']


class StockAdjustmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockAdjustment
        fields = ['id', 'item', 'quantity_change', 'reason', 'created_at']

    def validate_quantity_change(self, value):
        if value == 0:
            raise serializers.ValidationError("Quantity change cannot be zero.")
        return value
