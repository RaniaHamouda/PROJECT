from django.db import models
from django.contrib.auth.models import User 
 # أو استخدمي Custom User لو عايزة
 

class RoomType(models.Model):
    name = models.CharField(max_length=50)  # مثلاً "Single", "Double", "Suite"
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    title = models.CharField(max_length=100)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField(default=1)  # عدد الأشخاص الأقصى
    # لعرض عدة صور للغرفة نستخدم موديل منفصل للصور:
    # image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='rooms/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    capacity = models.IntegerField(default=1)  # الحقل الجديد

    def __str__(self):
        return f"Image for {self.room.title}"


class Customer(models.Model):
    # لو مش هتستخدميه كموديل المستخدم الأساسي، هتربطه مع User أو هتستخدمه بشكل مستقل
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # العلاقة مع المستخدم
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    # أي حقول إضافية زي العنوان، المدينة، الدولة:
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username



class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # حالة الدفع (مدفوع، غير مدفوع، ملغى)
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')

    def __str__(self):
        return f"{self.customer.user.username} booking {self.room.title}"


class Review(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(default=5)  # مثلاً من 1 إلى 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.customer.user.username} on {self.room.title}"


class Package(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # ممكن بريكات مرتبطة بغرفة أو مجموعة غرف أو مميزات إضافية
    rooms = models.ManyToManyField(Room, related_name='packages', blank=True)
    image = models.ImageField(upload_to='packages/', null=True, blank=True)

    def __str__(self):
        return self.title

    