from django.db import models

class Material(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    version = models.IntegerField(default=1) 
    
    def save(self, *args, **kwargs):
        # Increment version on update
        if self.pk:
            self.version += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order #{self.id}"

    def calculate_total_price(self):
        self.total_price = sum(
            item.calculate_discounted_price() for item in self.items.all()
        )
        self.save()


class OrderItem(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('flat', 'Flat'),
    ]

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Discount value
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, default='percentage')

    def calculate_discounted_price(self):
        if self.discount_type == 'percentage':
            discounted_price = self.quantity * self.price * (1 - self.discount / 100)
        elif self.discount_type == 'flat':
            discounted_price = self.quantity * self.price - self.discount
        else:
            discounted_price = self.quantity * self.price  # No discount
        return max(discounted_price, 0)  # Ensure price is not negative
    

class StockReport(models.Model):
    date = models.DateField(auto_now_add=True)
    report_file = models.FileField(upload_to="reports/stock_levels/")
    
class MaterialPriceHistory(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    price = models.FloatField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.material.name} - {self.price} (as of {self.effective_date})"

class MaterialUsage(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity_used = models.FloatField()
    date = models.DateField(auto_now_add=True)