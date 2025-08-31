from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ecommerce.models import Category, Product, Slide
from django.utils import timezone

class Command(BaseCommand):
    help = 'Create sample data for the E-Commerce application'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        try:
            # Create categories
            categories_data = [
                {'name': 'Electronics', 'description': 'Latest electronic gadgets and devices', 'slug': 'electronics'},
                {'name': 'Clothing', 'description': 'Fashion and apparel for all ages', 'slug': 'clothing'},
                {'name': 'Books', 'description': 'Books for all interests and ages', 'slug': 'books'},
                {'name': 'Home & Garden', 'description': 'Home improvement and garden supplies', 'slug': 'home-garden'},
            ]
            
            categories = {}
            for cat_data in categories_data:
                # Check if category already exists
                existing = Category.objects.filter(slug=cat_data['slug']).first()
                if existing:
                    categories[cat_data['slug']] = existing
                    self.stdout.write(f'Category already exists: {existing.name}')
                else:
                    category = Category.objects.create(**cat_data)
                    categories[cat_data['slug']] = category
                    self.stdout.write(f'Created category: {category.name}')
            
            # Create products
            products_data = [
                {
                    'name': 'Smartphone X1',
                    'description': 'Latest smartphone with advanced features and high-quality camera',
                    'price': 599.99,
                    'category': categories['electronics'],
                    'stock': 50,
                    'slug': 'smartphone-x1',
                    'images': ['https://via.placeholder.com/400x300/3B82F6/FFFFFF?text=Smartphone+X1']
                },
                {
                    'name': 'Laptop Pro',
                    'description': 'Professional laptop for work and gaming',
                    'price': 1299.99,
                    'category': categories['electronics'],
                    'stock': 25,
                    'slug': 'laptop-pro',
                    'images': ['https://via.placeholder.com/400x300/10B981/FFFFFF?text=Laptop+Pro']
                },
                {
                    'name': 'Casual T-Shirt',
                    'description': 'Comfortable cotton t-shirt for everyday wear',
                    'price': 24.99,
                    'category': categories['clothing'],
                    'stock': 100,
                    'slug': 'casual-t-shirt',
                    'images': ['https://via.placeholder.com/400x300/F59E0B/FFFFFF?text=Casual+T-Shirt']
                },
                {
                    'name': 'Denim Jeans',
                    'description': 'Classic denim jeans with perfect fit',
                    'price': 79.99,
                    'category': categories['clothing'],
                    'stock': 75,
                    'slug': 'denim-jeans',
                    'images': ['https://via.placeholder.com/400x300/6366F1/FFFFFF?text=Denim+Jeans']
                },
                {
                    'name': 'Programming Python',
                    'description': 'Comprehensive guide to Python programming',
                    'price': 39.99,
                    'category': categories['books'],
                    'stock': 30,
                    'slug': 'programming-python',
                    'images': ['https://via.placeholder.com/400x300/EF4444/FFFFFF?text=Programming+Python']
                },
                {
                    'name': 'Garden Tools Set',
                    'description': 'Complete set of essential garden tools',
                    'price': 89.99,
                    'category': categories['home-garden'],
                    'stock': 20,
                    'slug': 'garden-tools-set',
                    'images': ['https://via.placeholder.com/400x300/8B5CF6/FFFFFF?text=Garden+Tools+Set']
                },
            ]
            
            for prod_data in products_data:
                # Check if product already exists
                existing = Product.objects.filter(slug=prod_data['slug']).first()
                if existing:
                    self.stdout.write(f'Product already exists: {existing.name}')
                else:
                    product = Product.objects.create(**prod_data)
                    self.stdout.write(f'Created product: {product.name}')
            
            # Create slides
            slides_data = [
                {
                    'title': 'Welcome to E-Store',
                    'subtitle': 'Discover amazing products at great prices',
                    'image': 'https://via.placeholder.com/1200x400/3B82F6/FFFFFF?text=Welcome+to+E-Store',
                    'order': 1,
                    'is_active': True
                },
                {
                    'title': 'New Arrivals',
                    'subtitle': 'Check out our latest products',
                    'image': 'https://via.placeholder.com/1200x400/10B981/FFFFFF?text=New+Arrivals',
                    'order': 2,
                    'is_active': True
                },
                {
                    'title': 'Special Offers',
                    'subtitle': 'Limited time deals on selected items',
                    'image': 'https://via.placeholder.com/1200x400/F59E0B/FFFFFF?text=Special+Offers',
                    'order': 3,
                    'is_active': True
                },
            ]
            
            for slide_data in slides_data:
                # Check if slide already exists
                existing = Slide.objects.filter(title=slide_data['title']).first()
                if existing:
                    self.stdout.write(f'Slide already exists: {existing.title}')
                else:
                    slide = Slide.objects.create(**slide_data)
                    self.stdout.write(f'Created slide: {slide.title}')
            
            self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
            self.stdout.write('You can now access the application at http://localhost:8000')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating sample data: {e}'))
            self.stdout.write('You can still access the application at http://localhost:8000')
