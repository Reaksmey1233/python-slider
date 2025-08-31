from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Slide, Customer, Order, CartItem

# Note: Since we're using mongoengine Document models, we can't use Django's standard admin
# These models will be managed through custom views or a separate admin interface
# For now, we'll create simple admin views for demonstration

class CategoryAdmin:
    list_display = ['name', 'slug', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    
    def get_queryset(self):
        return Category.objects.all()

class SlideAdmin:
    list_display = ['title', 'order', 'is_active', 'image_preview', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'subtitle']
    ordering = ['order']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image)
        return "No Image"
    image_preview.short_description = 'Image Preview'
    
    def get_queryset(self):
        return Slide.objects.all()

class ProductAdmin:
    list_display = ['name', 'category', 'price', 'stock', 'is_active', 'main_image_preview', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    list_editable = ['price', 'stock', 'is_active']
    search_fields = ['name', 'description']
    
    def main_image_preview(self, obj):
        if obj.images:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.images[0])
        return "No Image"
    main_image_preview.short_description = 'Main Image'
    
    def get_queryset(self):
        return Product.objects.all()

class CustomerAdmin:
    list_display = ['user_id', 'phone', 'address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user_id', 'phone']
    
    def get_queryset(self):
        return Customer.objects.all()

class OrderAdmin:
    list_display = ['order_number', 'customer_id', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'customer_id']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    
    def get_queryset(self):
        return Order.objects.all()

class CartItemAdmin:
    list_display = ['product', 'quantity', 'session_key', 'created_at']
    list_filter = ['created_at']
    search_fields = ['product__name', 'session_key']
    
    def get_queryset(self):
        return CartItem.objects.all()

# Note: These admin classes are for reference only
# In a real application, you would need to create custom admin views
# or use a different approach to manage mongoengine models
