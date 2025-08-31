from mongoengine import Document, StringField, FloatField, IntField, ListField, ReferenceField, DateTimeField, BooleanField, ImageField
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
import os

class Category(Document):
    name = StringField(max_length=100, required=True)
    description = StringField(max_length=500)
    slug = StringField(max_length=100, unique=True)
    created_at = DateTimeField(default=timezone.now)
    
    meta = {
        'collection': 'categories',
        'ordering': ['name']
    }
    
    def __str__(self):
        return self.name

class Slide(Document):
    title = StringField(max_length=200)
    subtitle = StringField(max_length=200)
    image_url = StringField()  # Store image URL
    image_file = StringField()  # Store uploaded image file path
    # Legacy field support
    image = StringField()  # Keep for backward compatibility
    order = IntField(default=0)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=timezone.now)
    
    meta = {
        'collection': 'slides',
        'ordering': ['order']
    }
    
    def __str__(self):
        return self.title or f"Slide {self.order}"
    
    @property
    def image_display(self):
        """Return the image to display (file upload takes precedence)"""
        if self.image_file:
            # Normalize path separators for URLs
            return self.image_file.replace('\\', '/')
        if self.image_url:
            return self.image_url
        # Fallback to legacy field
        if hasattr(self, 'image') and self.image:
            return self.image
        return None
    
    def delete(self, *args, **kwargs):
        # Delete uploaded file when slide is deleted
        if self.image_file and os.path.exists(self.image_file):
            try:
                os.remove(self.image_file)
            except:
                pass
        super().delete(*args, **kwargs)

class Product(Document):
    name = StringField(max_length=200, required=True)
    description = StringField(max_length=1000)
    price = FloatField(required=True)
    category = ReferenceField(Category, required=True)
    image_urls = ListField(StringField())  # Store image URLs
    image_files = ListField(StringField())  # Store uploaded image file paths
    # Legacy field support
    images = ListField(StringField())  # Keep for backward compatibility
    stock = IntField(default=0)
    is_active = BooleanField(default=True)
    slug = StringField(max_length=200, unique=True)
    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(default=timezone.now)
    
    meta = {
        'collection': 'products',
        'ordering': ['-created_at']
    }
    
    def __str__(self):
        return self.name
    
    @property
    def images_display(self):
        """Return all images to display (file uploads take precedence)"""
        all_images = []
        if self.image_files:
            all_images.extend(self.image_files)
        if self.image_urls:
            all_images.extend(self.image_urls)
        # Fallback to legacy field
        if hasattr(self, 'images') and self.images:
            all_images.extend(self.images)
        return all_images
    
    def delete(self, *args, **kwargs):
        # Delete uploaded files when product is deleted
        if self.image_files:
            for image_path in self.image_files:
                if os.path.exists(image_path):
                    try:
                        os.remove(image_path)
                    except:
                        pass
        super().delete(*args, **kwargs)

class Customer(Document):
    user_id = IntField(required=True)  # Store Django User ID
    phone = StringField(max_length=20)
    address = StringField(max_length=500)
    created_at = DateTimeField(default=timezone.now)
    
    meta = {
        'collection': 'customers'
    }
    
    def __str__(self):
        try:
            user = User.objects.get(id=self.user_id)
            return f"{user.username} - {user.email}"
        except User.DoesNotExist:
            return f"User {self.user_id}"

class CartItem(Document):
    product = ReferenceField(Product, required=True)
    quantity = IntField(default=1, min_value=1)
    session_key = StringField(required=True)
    created_at = DateTimeField(default=timezone.now)
    
    meta = {
        'collection': 'cart_items'
    }
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class Order(Document):
    order_number = StringField(unique=True, default=lambda: f"ORD-{uuid.uuid4().hex[:8].upper()}")
    customer_id = IntField(required=True)  # Store Customer ID
    items = ListField(ReferenceField(CartItem))
    total_amount = FloatField(required=True)
    status = StringField(choices=['pending', 'processing', 'shipped', 'delivered', 'cancelled'], default='pending')
    shipping_address = StringField(max_length=500)
    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(default=timezone.now)
    
    meta = {
        'collection': 'orders',
        'ordering': ['-created_at']
    }
    
    def __str__(self):
        return f"Order {self.order_number}"
