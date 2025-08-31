
# E-Commerce Website with Django, Tailwind CSS, and MongoDB

A full-featured E-Commerce website built with Django, Tailwind CSS, and MongoDB using mongoengine.

## Features

### Frontend
- **Responsive Design**: Modern, mobile-friendly UI using Tailwind CSS
- **Home Page**: Carousel/slider with multiple product images
- **Product Listing**: Grid layout with category filtering
- **Product Details**: Image gallery, product information, and add to cart
- **Shopping Cart**: Update quantities and remove items
- **User Authentication**: Signup, login, and logout functionality

### Backend
- **Django Models**: Product, Category, Slide, Order, Customer, and Cart models
- **MongoDB Integration**: Using mongoengine for NoSQL database
- **Admin Dashboard**: Manage slides, products, categories, and orders
- **User Management**: Customer registration and authentication
- **Order Processing**: Complete checkout and order management

### Admin Features
- **Dashboard**: Overview of store statistics and recent orders
- **Product CRUD**: Create, Read, Update, Delete products with full form validation
- **Slide CRUD**: Create, Read, Update, Delete carousel slides with image previews
- **Category Management**: Organize products by categories
- **Order Management**: View and update order statuses
- **Image Previews**: Visual previews in admin interface
- **Stock Management**: Monitor low stock products
- **User Management**: Customer registration and authentication

## Image Management

The application now supports both image file uploads and image URLs, providing flexibility for different use cases:

### File Uploads
- **Direct Upload**: Upload image files directly from your computer
- **Supported Formats**: JPG, PNG, GIF
- **Automatic Storage**: Images are stored in the `media/` directory
- **Unique Naming**: Files are automatically renamed to prevent conflicts
- **Local Storage**: Images are served from your local server

### Image URLs
- **External Images**: Use images hosted on external services
- **Flexibility**: Link to images from CDNs, social media, or other websites
- **No Storage**: No local storage required
- **Quick Setup**: Just paste the image URL

### Hybrid Approach
- **Combined Usage**: Use both uploads and URLs for the same product/slide
- **Priority System**: File uploads take precedence over URLs
- **Fallback Support**: Gracefully handles missing or invalid images
- **Legacy Support**: Maintains compatibility with existing data

### File Organization
```
media/
├── products/     # Product images
└── slides/       # Carousel slide images
```

### Benefits
- **Flexibility**: Choose the best approach for your needs
- **Performance**: Local files load faster than external URLs
- **Reliability**: Local files are always available
- **Cost-Effective**: No external hosting costs for local files
- **Control**: Full control over image quality and availability

## Technology Stack

- **Backend**: Django 5.2.5
- **Database**: MongoDB with mongoengine
- **Frontend**: Tailwind CSS (CDN)
- **Icons**: Font Awesome
- **Authentication**: Django's built-in auth system

## Prerequisites

- Python 3.8 or higher
- MongoDB server running locally or remotely
- pip (Python package installer)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DjangoProject2
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MongoDB**
   - Install MongoDB on your system
   - Start MongoDB service
   - Create a database named `ecommerce_db`

5. **Configure Django settings**
   - Update database settings in `Ecommerce_project/settings.py` if needed
   - Ensure MongoDB is running on `localhost:27017`

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Main site: http://localhost:8000
   - Admin dashboard: http://localhost:8000/dashboard
   - Django admin: http://localhost:8000/admin
   - Product management: http://localhost:8000/manage/products/
   - Slide management: http://localhost:8000/manage/slides/

## Project Structure

```
DjangoProject2/
├── Ecommerce_project/          # Main Django project
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL configuration
│   └── ...
├── ecommerce/                 # E-commerce app
│   ├── models.py              # MongoDB models
│   ├── views.py               # View functions
│   ├── urls.py                # App URL patterns
│   └── admin.py               # Admin configuration
├── templates/                 # HTML templates
│   ├── base.html              # Base template
│   └── ecommerce/             # App templates
├── static/                    # Static files
├── media/                     # Uploaded files
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Usage

### Setting up the Admin Dashboard

1. **Access the admin panel**: http://localhost:8000/admin
2. **Login with your superuser credentials**
3. **Add categories**: Create product categories
4. **Add slides**: Upload images for the home page carousel
5. **Add products**: Create products with images and details

### Using Image Uploads

#### For Products:
1. **Go to Product Management**: http://localhost:8000/manage/products/
2. **Click "Add New Product"**
3. **Fill in product details**
4. **Upload Images**: Use the "Upload Images" field to select image files
5. **Add Image URLs**: Optionally add external image URLs in the "Image URLs" field
6. **Save**: The product will display uploaded images first, then URL images

#### For Slides:
1. **Go to Slide Management**: http://localhost:8000/manage/slides/
2. **Click "Add New Slide"**
3. **Fill in slide details**
4. **Upload Image**: Use the "Upload Image" field to select an image file
5. **Add Image URL**: Optionally add an external image URL
6. **Save**: The slide will display the uploaded image if available, otherwise the URL

#### Image Upload Tips:
- **Supported Formats**: JPG, PNG, GIF
- **File Size**: Keep images under 5MB for best performance
- **Dimensions**: Recommended sizes:
  - **Products**: 800x600 pixels or larger
  - **Slides**: 1200x600 pixels or larger
- **Quality**: Use high-quality images for better presentation
- **Naming**: Files are automatically renamed to prevent conflicts

### Customer Features

1. **Browse products**: View all products or filter by category
2. **Product details**: Click on products to see full details
3. **Add to cart**: Add products to shopping cart
4. **Manage cart**: Update quantities or remove items
5. **User registration**: Create customer accounts
6. **Checkout**: Complete orders with shipping information
7. **Order history**: View past orders and status

## Database Models

### Category
- name, description, slug, created_at

### Product
- name, description, price, category, images, stock, slug, is_active

### Slide
- title, subtitle, image, order, is_active

### Customer
- user (Django User), phone, address

### CartItem
- product, quantity, session_key

### Order
- order_number, customer, items, total_amount, status, shipping_address

## Customization

### Adding New Features

1. **New Models**: Add to `ecommerce/models.py`
2. **New Views**: Add to `ecommerce/views.py`
3. **New URLs**: Add to `ecommerce/urls.py`
4. **New Templates**: Create in `templates/ecommerce/`

### Styling

- The project uses Tailwind CSS via CDN
- Custom styles can be added in template `{% block extra_css %}`
- Color scheme can be modified in the Tailwind config

### Database

- MongoDB connection settings in `settings.py`
- Models use mongoengine Document classes
- Collections are automatically created

## Deployment

### Production Settings

1. **Update settings.py**:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use environment variables for sensitive data

2. **Static files**:
   - Run `python manage.py collectstatic`
   - Configure web server to serve static files

3. **Database**:
   - Use MongoDB Atlas or self-hosted MongoDB
   - Update connection settings

4. **Web server**:
   - Use Gunicorn or uWSGI
   - Configure Nginx or Apache as reverse proxy

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support and questions, please open an issue in the repository.
