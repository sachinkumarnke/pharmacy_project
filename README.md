# 🏥 Pharmacy Management System

A comprehensive Django-based pharmacy management system with e-commerce functionality, admin panel, and Docker deployment.

![Pharmacy System Banner](screenshots/banner.png)

## 🌟 Features

### 🛒 E-Commerce Functionality
- **Product Catalog** with categories, brands, and manufacturers
- **Shopping Cart** and **Wishlist** management
- **Advanced Search** with filters and sorting
- **Coupon System** with discount management
- **Multi-step Checkout** process
- **Order Management** and tracking

![Homepage Screenshot](screenshots/homepage.png)

### 👨‍⚕️ Healthcare Features
- **Doctor Profiles** with specializations and photos
- **Prescription Management** system
- **Health Tips** and emergency contacts
- **Product Reviews** and ratings
- **Customer Notifications**

![Doctor Profiles](screenshots/doctors.png)

### 🔐 User Management
- **Combined Login/Register** system with toggle
- **Customer Profiles** with order history
- **Admin Dashboard** with comprehensive controls
- **Role-based Access** control

![Authentication System](screenshots/auth.png)

### 📱 Responsive Design
- **Cross-browser Compatible** (Chrome, Firefox, Safari, Edge, IE11)
- **Mobile-first Design** with Bootstrap 5.3.0
- **Touch-friendly Interface**
- **Optimized Performance**

![Responsive Design](screenshots/responsive.png)

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Django 5.2.3 |
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap 5.3.0 |
| **Database** | PostgreSQL 15 / SQLite |
| **Containerization** | Docker & Docker Compose |
| **Image Processing** | Pillow 10.0.0 |

## 📁 Project Structure

```
pharmacy_project/
├── 📁 pharmacy/                 # Main Django app
│   ├── 📁 templates/           # HTML templates
│   ├── 📁 static/              # CSS, JS, images
│   ├── 📄 models.py            # Database models
│   ├── 📄 views.py             # Business logic
│   └── 📄 admin.py             # Admin interface
├── 📁 media/                   # User uploads
├── 📄 docker-compose.yml       # Container orchestration
├── 📄 Dockerfile              # Container configuration
├── 📄 requirements.txt         # Python dependencies
└── 📄 manage.py               # Django management
```

## 🚀 Quick Start

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pharmacy_project
   ```

2. **Start with Docker**
   ```bash
   docker compose up -d
   ```

3. **Access the application**
   - Website: http://localhost:8000
   - Admin: http://localhost:8000/admin

![Docker Setup](screenshots/docker.png)

### Option 2: Local Development

1. **Install Python 3.11+**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

## 📊 Database Models

### Core Models
- **Product**: Main product catalog with pricing, stock, and details
- **Category**: Product categorization system
- **Brand & Manufacturer**: Product brand and manufacturer tracking
- **Doctor**: Healthcare professional profiles

### E-Commerce Models
- **Order & OrderItem**: Order management system
- **Wishlist**: Customer wishlist functionality
- **Coupon**: Discount and promotion system
- **PaymentMethod**: Payment options management

### User Models
- **Customer**: Extended user profiles
- **Review**: Product reviews and ratings
- **Notification**: Customer notification system

![Database Schema](screenshots/database.png)

## 🎨 Screenshots

### Homepage with Search and Categories
![Homepage Features](screenshots/homepage-features.png)

### Product Catalog
![Product Catalog](screenshots/products.png)

### Shopping Cart and Checkout
![Shopping Cart](screenshots/cart.png)
![Checkout Process](screenshots/checkout.png)

### Admin Dashboard
![Admin Dashboard](screenshots/admin.png)

### Wishlist Management
![Wishlist](screenshots/wishlist.png)

### Advanced Search
![Advanced Search](screenshots/search.png)

## 🔧 Configuration

### Environment Variables
```env
DEBUG=1
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost/pharmacy_db
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Docker Configuration
```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=pharmacy_db
```

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

For Docker:
```bash
docker compose exec web python manage.py test
```

## 📈 Performance Features

- **Optimized Database Queries** with proper indexing
- **Static File Management** with collectstatic
- **Image Optimization** with Pillow
- **Responsive Caching** ready implementation
- **Cross-browser Compatibility** tested

## 🔒 Security Features

- **CSRF Protection** on all forms
- **SQL Injection Prevention** with Django ORM
- **XSS Protection** with template auto-escaping
- **Secure Authentication** system
- **Input Validation** and sanitization

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up environment variables
- [ ] Configure SSL/HTTPS
- [ ] Set up database backups
- [ ] Configure static file serving

### Docker Production
```bash
docker compose -f docker-compose.prod.yml up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 API Documentation

### Key Endpoints
- `GET /` - Homepage
- `GET /products/` - Product listing
- `POST /add-to-cart/` - Add to cart
- `GET /wishlist/` - User wishlist
- `POST /checkout/` - Checkout process

## 🔄 Updates and Maintenance

### Regular Tasks
- Database backups
- Security updates
- Performance monitoring
- User feedback review

### Version History
- **v1.0.0** - Initial release with core features
- **v1.1.0** - Added Docker support
- **v1.2.0** - Enhanced e-commerce features

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting guide
- Review the project documentation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap team for the responsive CSS framework
- PostgreSQL team for the robust database system
- Docker team for containerization technology

---

**Built with ❤️ using Django and modern web technologies**

![Footer](screenshots/footer.png)