from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Customer)

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone', 'email', )




