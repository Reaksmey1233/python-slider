from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Product, Category, Slide, CartItem, Customer, Order
from django.utils import timezone
import json
import os
import uuid
from django.conf import settings

def home(request):
    """Home page with carousel and featured products"""
    slides = Slide.objects.filter(is_active=True).order_by('order')
    featured_products = Product.objects.filter(is_active=True)[:8]
    categories = Category.objects.all()
    
    context = {
        'slides': slides,
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'ecommerce/home.html', context)

def product_list(request, category_slug=None):
    """Product listing page with category filtering"""
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)
    
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        except Category.DoesNotExist:
            from django.http import Http404
            raise Http404("Category not found")
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category_slug,
    }
    return render(request, 'ecommerce/product_list.html', context)

def product_detail(request, product_slug):
    """Product detail page"""
    try:
        product = Product.objects.get(slug=product_slug, is_active=True)
        related_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]
    except Product.DoesNotExist:
        from django.http import Http404
        raise Http404("Product not found")
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'ecommerce/product_detail.html', context)

def cart(request):
    """Cart page"""
    if not request.session.session_key:
        request.session.create()
    
    cart_items = CartItem.objects.filter(session_key=request.session.session_key)
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'ecommerce/cart.html', context)

@csrf_exempt
def add_to_cart(request):
    """Add product to cart"""
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        if not request.session.session_key:
            request.session.create()
        
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            
            # Check if item already in cart
            existing_cart_item = CartItem.objects.filter(
                product=product,
                session_key=request.session.session_key
            ).first()
            
            if existing_cart_item:
                existing_cart_item.quantity += quantity
                existing_cart_item.save()
                cart_item = existing_cart_item
            else:
                cart_item = CartItem.objects.create(
                    product=product,
                    session_key=request.session.session_key,
                    quantity=quantity
                )
            
            # Remove the old logic since we handle it above
            
            return JsonResponse({'success': True, 'message': 'Product added to cart'})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@csrf_exempt
def update_cart(request):
    """Update cart item quantity"""
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
        
        try:
            cart_item = CartItem.objects.get(id=item_id, session_key=request.session.session_key)
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
            
            return JsonResponse({'success': True})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Cart item not found'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

@csrf_exempt
def remove_from_cart(request):
    """Remove item from cart"""
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        
        try:
            cart_item = CartItem.objects.get(id=item_id, session_key=request.session.session_key)
            cart_item.delete()
            return JsonResponse({'success': True})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Cart item not found'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def user_signup(request):
    """User registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'ecommerce/signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'ecommerce/signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'ecommerce/signup.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        Customer.objects.create(user_id=user.id)
        
        login(request, user)
        messages.success(request, 'Account created successfully')
        return redirect('home')
    
    return render(request, 'ecommerce/signup.html')

def user_login(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'ecommerce/login.html')

def user_logout(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')

@login_required
def checkout(request):
    """Checkout page"""
    if not request.session.session_key:
        return redirect('cart')
    
    cart_items = CartItem.objects.filter(session_key=request.session.session_key)
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty')
        return redirect('cart')
    
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        
        if not shipping_address:
            messages.error(request, 'Please provide shipping address')
            return render(request, 'ecommerce/checkout.html', {'cart_items': cart_items, 'total': total})
        
        # Create order
        existing_customer = Customer.objects.filter(user_id=request.user.id).first()
        if existing_customer:
            customer = existing_customer
        else:
            customer = Customer.objects.create(user_id=request.user.id)
        order = Order.objects.create(
            customer_id=str(customer.id),
            items=cart_items,
            total_amount=total,
            shipping_address=shipping_address
        )
        
        # Clear cart
        cart_items.delete()
        
        messages.success(request, f'Order placed successfully! Order number: {order.order_number}')
        return redirect('order_confirmation', order_id=order.id)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'ecommerce/checkout.html', context)

@login_required
def order_confirmation(request, order_id):
    """Order confirmation page"""
    try:
        customer = Customer.objects.get(user_id=request.user.id)
        order = Order.objects.get(id=order_id, customer_id=str(customer.id))
    except (Customer.DoesNotExist, Order.DoesNotExist):
        from django.http import Http404
        raise Http404("Order not found")
    return render(request, 'ecommerce/order_confirmation.html', {'order': order})

@login_required
def my_orders(request):
    """User's order history"""
    existing_customer = Customer.objects.filter(user_id=request.user.id).first()
    if existing_customer:
        customer = existing_customer
    else:
        customer = Customer.objects.create(user_id=request.user.id)
    
    # Convert customer.id to string for proper comparison
    orders = Order.objects.filter(customer_id=str(customer.id)).order_by('-created_at')
    return render(request, 'ecommerce/my_orders.html', {'orders': orders})

@login_required
def dashboard(request):
    """Admin dashboard for managing products, categories, and slides"""
    # Check if user is staff/admin
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    # Get statistics
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_orders = Order.objects.count()
    total_customers = Customer.objects.count()
    
    # Get recent orders
    recent_orders = Order.objects.order_by('-created_at')[:5]
    
    # Get low stock products
    low_stock_products = Product.objects.filter(stock__lt=10, is_active=True)[:5]
    
    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'ecommerce/dashboard.html', context)

# ==================== PRODUCT CRUD OPERATIONS ====================

@login_required
def product_list_admin(request):
    """Admin view for listing all products"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'ecommerce/admin/product_list.html', {'products': products})

@login_required
def product_create(request):
    """Create a new product"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        category_id = request.POST.get('category')
        image_urls = request.POST.get('image_urls', '').split(',') if request.POST.get('image_urls') else []
        is_active = request.POST.get('is_active') == 'on'
        
        # Clean up image URLs (remove empty strings)
        image_urls = [url.strip() for url in image_urls if url.strip()]
        
        try:
            category = Category.objects.get(id=category_id)
            
            # Handle file uploads
            image_files = []
            if request.FILES:
                for uploaded_file in request.FILES.getlist('image_files'):
                    if uploaded_file:
                        # Create media directory if it doesn't exist
                        media_dir = os.path.join(settings.MEDIA_ROOT, 'products')
                        os.makedirs(media_dir, exist_ok=True)
                        
                        # Generate unique filename
                        file_extension = os.path.splitext(uploaded_file.name)[1]
                        filename = f"product_{uuid.uuid4().hex}{file_extension}"
                        file_path = os.path.join(media_dir, filename)
                        
                        # Save file
                        with open(file_path, 'wb+') as destination:
                            for chunk in uploaded_file.chunks():
                                destination.write(chunk)
                        
                        # Store relative path for database
                        relative_path = os.path.join('media', 'products', filename)
                        image_files.append(relative_path)
            
            product = Product.objects.create(
                name=name,
                description=description,
                price=float(price),
                stock=int(stock),
                category=category,
                image_urls=image_urls,
                image_files=image_files,
                is_active=is_active
            )
            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('product_list_admin')
        except Exception as e:
            messages.error(request, f'Error creating product: {str(e)}')
    
    categories = Category.objects.all()
    return render(request, 'ecommerce/admin/product_form.html', {'categories': categories, 'action': 'Create'})

@login_required
def product_update(request, product_id):
    """Update an existing product"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, 'Product not found.')
        return redirect('product_list_admin')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        category_id = request.POST.get('category')
        image_urls = request.POST.get('image_urls', '').split(',') if request.POST.get('image_urls') else []
        is_active = request.POST.get('is_active') == 'on'
        
        # Clean up image URLs (remove empty strings)
        image_urls = [url.strip() for url in image_urls if url.strip()]
        
        try:
            category = Category.objects.get(id=category_id)
            
            # Handle file uploads
            image_files = list(product.image_files) if product.image_files else []  # Keep existing files
            if request.FILES:
                for uploaded_file in request.FILES.getlist('image_files'):
                    if uploaded_file:
                        # Create media directory if it doesn't exist
                        media_dir = os.path.join(settings.MEDIA_ROOT, 'products')
                        os.makedirs(media_dir, exist_ok=True)
                        
                        # Generate unique filename
                        file_extension = os.path.splitext(uploaded_file.name)[1]
                        filename = f"product_{uuid.uuid4().hex}{file_extension}"
                        file_path = os.path.join(media_dir, filename)
                        
                        # Save file
                        with open(file_path, 'wb+') as destination:
                            for chunk in uploaded_file.chunks():
                                destination.write(chunk)
                        
                        # Store relative path for database
                        relative_path = os.path.join('media', 'products', filename)
                        image_files.append(relative_path)
            
            product.name = name
            product.description = description
            product.price = float(price)
            product.stock = int(stock)
            product.category = category
            product.image_urls = image_urls
            product.image_files = image_files
            product.is_active = is_active
            product.save()
            
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('product_list_admin')
        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')
    
    categories = Category.objects.all()
    return render(request, 'ecommerce/admin/product_form.html', {
        'product': product, 
        'categories': categories, 
        'action': 'Update'
    })

@login_required
def product_delete(request, product_id):
    """Delete a product"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    try:
        product = Product.objects.get(id=product_id)
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
    except Product.DoesNotExist:
        messages.error(request, 'Product not found.')
    except Exception as e:
        messages.error(request, f'Error deleting product: {str(e)}')
    
    return redirect('product_list_admin')

# ==================== SLIDE CRUD OPERATIONS ====================

@login_required
def slide_list_admin(request):
    """Admin view for listing all slides"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    slides = Slide.objects.all().order_by('order')
    return render(request, 'ecommerce/admin/slide_list.html', {'slides': slides})

@login_required
def slide_create(request):
    """Create a new slide"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')
        image_url = request.POST.get('image_url', '').strip()
        order = request.POST.get('order', 0)
        is_active = request.POST.get('is_active') == 'on'
        
        try:
            # Handle file upload
            image_file = None
            if request.FILES and 'image_file' in request.FILES:
                uploaded_file = request.FILES['image_file']
                if uploaded_file:
                    # Create media directory if it doesn't exist
                    media_dir = os.path.join(settings.MEDIA_ROOT, 'slides')
                    os.makedirs(media_dir, exist_ok=True)
                    
                    # Generate unique filename
                    file_extension = os.path.splitext(uploaded_file.name)[1]
                    filename = f"slide_{uuid.uuid4().hex}{file_extension}"
                    file_path = os.path.join(media_dir, filename)
                    
                    # Save file
                    with open(file_path, 'wb+') as destination:
                        for chunk in uploaded_file.chunks():
                            destination.write(chunk)
                    
                    # Store relative path for database
                    image_file = os.path.join('media', 'slides', filename)
            
            slide = Slide.objects.create(
                title=title,
                subtitle=subtitle,
                image_url=image_url if image_url else None,
                image_file=image_file,
                order=int(order),
                is_active=is_active
            )
            messages.success(request, f'Slide "{slide.title}" created successfully!')
            return redirect('slide_list_admin')
        except Exception as e:
            messages.error(request, f'Error creating slide: {str(e)}')
    
    return render(request, 'ecommerce/admin/slide_form.html', {'action': 'Create'})

@login_required
def slide_update(request, slide_id):
    """Update an existing slide"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    try:
        slide = Slide.objects.get(id=slide_id)
    except Slide.DoesNotExist:
        messages.error(request, 'Slide not found.')
        return redirect('slide_list_admin')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle')
        image_url = request.POST.get('image_url', '').strip()
        order = request.POST.get('order', 0)
        is_active = request.POST.get('is_active') == 'on'
        
        try:
            # Handle file upload
            image_file = slide.image_file  # Keep existing file
            if request.FILES and 'image_file' in request.FILES:
                uploaded_file = request.FILES['image_file']
                if uploaded_file:
                    # Create media directory if it doesn't exist
                    media_dir = os.path.join(settings.MEDIA_ROOT, 'slides')
                    os.makedirs(media_dir, exist_ok=True)
                    
                    # Generate unique filename
                    file_extension = os.path.splitext(uploaded_file.name)[1]
                    filename = f"slide_{uuid.uuid4().hex}{file_extension}"
                    file_path = os.path.join(media_dir, filename)
                    
                    # Save file
                    with open(file_path, 'wb+') as destination:
                        for chunk in uploaded_file.chunks():
                            destination.write(chunk)
                    
                    # Store relative path for database
                    image_file = os.path.join('media', 'slides', filename)
            
            slide.title = title
            slide.subtitle = subtitle
            slide.image_url = image_url if image_url else None
            slide.image_file = image_file
            slide.order = int(order)
            slide.is_active = is_active
            slide.save()
            
            messages.success(request, f'Slide "{slide.title}" updated successfully!')
            return redirect('slide_list_admin')
        except Exception as e:
            messages.error(request, f'Error updating slide: {str(e)}')
    
    return render(request, 'ecommerce/admin/slide_form.html', {
        'slide': slide, 
        'action': 'Update'
    })

@login_required
def slide_delete(request, slide_id):
    """Delete a slide"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    try:
        slide = Slide.objects.get(id=slide_id)
        slide_title = slide.title
        slide.delete()
        messages.success(request, f'Slide "{slide_title}" deleted successfully!')
    except Slide.DoesNotExist:
        messages.error(request, 'Slide not found.')
    except Exception as e:
        messages.error(request, f'Error deleting slide: {str(e)}')
    
    return redirect('slide_list_admin')
