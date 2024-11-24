from django.db import models

class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class InventoryItem(BaseModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name="items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    
    def __str__(self):
        return self.name


class StockAdjustment(BaseModel):
    item = models.ForeignKey(InventoryItem, related_name="stock_adjustments", on_delete=models.CASCADE)
    quantity_change = models.IntegerField()
    reason = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.item.name} - {self.quantity_change}"
