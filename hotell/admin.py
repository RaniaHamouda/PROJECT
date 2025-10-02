from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Room, Customer, Booking
from django.contrib import admin
from .models import Customer
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone", "user")
admin.site.register(Room)
admin.site.register(Booking)



# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ("id", "name", "email", "phone", "user")
