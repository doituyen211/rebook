from django.db import models

class Genres(models.Model):
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'genres'

class Customers(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'buyers'


class BookStatus(models.TextChoices):
    AVAILABLE = 'available', 'Available'
    SOLD = 'sold', 'Sold'
    UNAVAILABLE = 'unavailable', 'Unavailable'
        
class Books(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    publishing_house = models.CharField(max_length=255, blank=True, null=True)
    publishing_year = models.DateField(blank=True, null=True)
    pages = models.IntegerField(blank=True, null=True)
    genre = models.ForeignKey('Genres', on_delete=models.SET_NULL, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=BookStatus.choices, default=BookStatus.AVAILABLE)
    seller = models.ForeignKey('Customers', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'books'


class OrderStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'

class Orders(models.Model):
    buyer = models.ForeignKey('Customers', on_delete=models.SET_NULL, blank=True, null=True)
    total_value = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"order: {self.buyer} + {self.total_value} + {self.order_status}"
    
    class Meta:
        db_table = 'orders'


class OrderItems(models.Model):
    order = models.ForeignKey('Orders', on_delete=models.CASCADE)
    book = models.ForeignKey('Books', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __init__(self):
        return f"Order Item: {self.book.name} x {self.quantity}"

    class Meta:
        db_table = 'order_items'


class PaymentMethod(models.TextChoices):
    ONLINE = 'online', 'Online'
    COD = 'COD', 'Cash on Delivery'

class PaymentStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    PAID = 'paid', 'Paid'
    FAILED = 'failed', 'Failed'

class Payments(models.Model):
    order = models.OneToOneField('Orders', on_delete=models.CASCADE, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices)
    payment_status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __init__(self):
        return f"Payment for Order {self.order.id} - {self.payment_status}"

    class Meta:
        db_table = 'payments'



