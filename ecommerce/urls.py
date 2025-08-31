from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<str:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<str:product_slug>/', views.product_detail, name='product_detail'),
    
    # Cart functionality
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    
    # User authentication
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Checkout and orders
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<str:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('my-orders/', views.my_orders, name='my_orders'),
    
    # Admin dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Admin Product CRUD
    path('manage/products/', views.product_list_admin, name='product_list_admin'),
    path('manage/products/create/', views.product_create, name='product_create'),
    path('manage/products/<str:product_id>/update/', views.product_update, name='product_update'),
    path('manage/products/<str:product_id>/delete/', views.product_delete, name='product_delete'),
    
    # Admin Slide CRUD
    path('manage/slides/', views.slide_list_admin, name='slide_list_admin'),
    path('manage/slides/create/', views.slide_create, name='slide_create'),
    path('manage/slides/<str:slide_id>/update/', views.slide_update, name='slide_update'),
    path('manage/slides/<str:slide_id>/delete/', views.slide_delete, name='slide_delete'),
]
