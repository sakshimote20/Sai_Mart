from django.contrib import admin
from .models import Product, Order, Feedback

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'unit', 'special_offer')
    search_fields = ('name',)
    list_filter = ('unit', 'special_offer')

admin.site.register(Product, ProductAdmin)  # Only register once
admin.site.register(Order)
admin.site.register(Feedback)
