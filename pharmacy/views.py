from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Avg
from .models import Product, Category, UserProfile, Wishlist, Coupon, PaymentMethod

# Home page view
def home(request):
    from .models import Banner
    featured_products = Product.objects.filter(stock__gt=0)[:4]  # Get 4 products with stock
    categories = Category.objects.all()
    banners = Banner.objects.filter(is_active=True).order_by('order', 'created_at')
    return render(request, 'pharmacy/home.html', {
        'featured_products': featured_products,
        'categories': categories,
        'banners': banners
    })

# View to display a list of all products with search and filtering
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            name__icontains=search_query
        ) | products.filter(
            description__icontains=search_query
        ) | products.filter(
            category__name__icontains=search_query
        )
    
    # Category filtering
    category_param = request.GET.get('category')
    if category_param:
        try:
            # Try to filter by category ID
            category_id = int(category_param)
            products = products.filter(category_id=category_id)
        except ValueError:
            # Filter by category name if not a number
            products = products.filter(category__name__icontains=category_param)
    
    # Order by name
    products = products.order_by('name')
    
    return render(request, 'pharmacy/product_list.html', {
        'products': products,
        'categories': categories
    })

# View to display details of a specific product
def product_detail(request, pk):
    from .models import ProductComment
    product = get_object_or_404(Product, pk=pk)
    comments = ProductComment.objects.filter(product=product).order_by('-created_at')
    suggested_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    # Handle comment submission
    if request.method == 'POST' and request.user.is_authenticated:
        comment_text = request.POST.get('comment')
        rating = request.POST.get('rating', 5)
        if comment_text:
            ProductComment.objects.create(
                product=product,
                user=request.user,
                comment=comment_text,
                rating=int(rating)
            )
            messages.success(request, 'Your review has been added!')
            return redirect('pharmacy:product_detail', pk=pk)
    
    return render(request, 'pharmacy/product_detail.html', {
        'product': product,
        'comments': comments,
        'suggested_products': suggested_products
    })

# About page view
def about(request):
    return render(request, 'pharmacy/about.html')

# Contact page view
def contact(request):
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # In a real application, you would save this to database or send email
        messages.success(request, f'Thank you {name}! Your message has been sent. We will get back to you soon.')
        return redirect('pharmacy:contact')
    
    return render(request, 'pharmacy/contact.html')

# Prescriptions page view
def prescriptions(request):
    from .models import Doctor, Specialization
    doctors = Doctor.objects.filter(is_active=True).select_related('specialization')
    specializations = Specialization.objects.all()
    
    if request.method == 'POST':
        try:
            from .models import Prescription
            
            # Get form data
            patient_name = request.POST.get('patient_name')
            patient_phone = request.POST.get('patient_phone')
            patient_email = request.POST.get('patient_email')
            doctor_name = request.POST.get('doctor_name')
            prescription_image = request.FILES.get('prescription_image')
            delivery_address = request.POST.get('delivery_address')
            special_instructions = request.POST.get('special_instructions', '')
            is_urgent = request.POST.get('urgent') == 'on'
            
            # Try to find matching doctor
            doctor = None
            if doctor_name:
                doctor = Doctor.objects.filter(name__icontains=doctor_name, is_active=True).first()
            
            # Create prescription
            prescription = Prescription.objects.create(
                user=request.user if request.user.is_authenticated else None,
                doctor=doctor,
                patient_name=patient_name,
                patient_phone=patient_phone,
                patient_email=patient_email,
                doctor_name=doctor_name,
                image=prescription_image,
                delivery_address=delivery_address,
                special_instructions=special_instructions,
                is_urgent=is_urgent
            )
            
            messages.success(request, f'Thank you {patient_name}! Your prescription has been uploaded successfully. We will process it within 2-4 hours.')
            return redirect('pharmacy:prescriptions')
            
        except Exception as e:
            messages.error(request, f'Error uploading prescription: {str(e)}')
    
    return render(request, 'pharmacy/prescriptions.html', {
        'doctors': doctors,
        'specializations': specializations
    })

# View to add a product to the cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if product.stock > 0:
        # Initialize cart in session if it doesn't exist
        if 'cart' not in request.session:
            request.session['cart'] = {}
        
        cart = request.session['cart']
        product_id_str = str(product_id)
        
        # Add or update product in cart
        if product_id_str in cart:
            cart[product_id_str] += 1
        else:
            cart[product_id_str] = 1
        
        request.session['cart'] = cart
        request.session.modified = True
        
        messages.success(request, f'{product.name} has been added to your cart!')
    else:
        messages.error(request, f'Sorry, {product.name} is out of stock.')
    
    # Redirect back to the previous page or product list
    return redirect(request.META.get('HTTP_REFERER', 'pharmacy:product_list'))

# View to display the shopping cart
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            item_total = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total
            })
            total_price += item_total
        except Product.DoesNotExist:
            continue
    
    return render(request, 'pharmacy/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

# Combined Authentication view
def auth_view(request):
    if request.user.is_authenticated:
        return redirect('pharmacy:home')
    return render(request, 'pharmacy/auth.html')

# Authentication views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('pharmacy:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Try to authenticate with username (email)
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('pharmacy:home')
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'pharmacy/auth.html')
    
    return render(request, 'pharmacy/auth.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('pharmacy:home')
    
    if request.method == 'POST':
        try:
            from django.contrib.auth.models import User
            
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            address = request.POST.get('address', '')
            city = request.POST.get('city', '')
            zip_code = request.POST.get('zip_code', '')
            newsletter = request.POST.get('newsletter') == 'on'
            
            # Validation
            if not all([first_name, last_name, email, mobile, password1, password2]):
                messages.error(request, 'Please fill in all required fields.')
                return render(request, 'pharmacy/auth.html')
            
            if password1 != password2:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'pharmacy/auth.html')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
                return render(request, 'pharmacy/auth.html')
            
            if len(password1) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                return render(request, 'pharmacy/auth.html')
            
            # Create user
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                mobile=mobile,
                address=address,
                city=city,
                zip_code=zip_code,
                newsletter=newsletter
            )
            
            messages.success(request, f'Account created successfully! Please login to continue.')
            return render(request, 'pharmacy/auth.html')
            
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
    
    return render(request, 'pharmacy/auth.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('pharmacy:home')

# View to remove item from cart
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        product = get_object_or_404(Product, id=product_id)
        del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f'{product.name} removed from cart!')
    
    return redirect('pharmacy:cart')

# View to decrease item quantity in cart
def decrease_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        if cart[product_id_str] > 1:
            cart[product_id_str] -= 1
            request.session['cart'] = cart
            request.session.modified = True
            messages.success(request, 'Quantity updated!')
        else:
            # If quantity is 1, remove the item
            return remove_from_cart(request, product_id)
    
    return redirect('pharmacy:cart')

# View to clear entire cart
def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    messages.success(request, 'Cart cleared!')
    return redirect('pharmacy:cart')

# Doctors page view
def doctors(request):
    from .models import Doctor, Specialization
    
    doctors = Doctor.objects.filter(is_active=True).select_related('specialization')
    specializations = Specialization.objects.all()
    
    # Filter by specialization
    specialization_id = request.GET.get('specialization')
    if specialization_id:
        doctors = doctors.filter(specialization_id=specialization_id)
    
    # Order by name
    doctors = doctors.order_by('name')
    
    return render(request, 'pharmacy/doctors.html', {
        'doctors': doctors,
        'specializations': specializations
    })

# User profile view
@login_required
def profile(request):
    from .models import Order, Prescription, ProductComment
    
    # Get user data
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    prescriptions = Prescription.objects.filter(user=user).order_by('-uploaded_at')
    reviews = ProductComment.objects.filter(user=user)
    
    # Calculate stats
    orders_count = orders.count()
    prescriptions_count = prescriptions.count()
    reviews_count = reviews.count()
    total_spent = sum(order.total_price for order in orders if order.is_paid)
    recent_orders = orders[:5]
    
    # Handle profile update
    if request.method == 'POST':
        try:
            # Update user info
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.save()
            
            # Update or create user profile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.mobile = request.POST.get('mobile', '')
            profile.address = request.POST.get('address', '')
            profile.city = request.POST.get('city', '')
            profile.zip_code = request.POST.get('zip_code', '')
            profile.save()
            
            messages.success(request, 'Profile updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
        
        return redirect('pharmacy:profile')
    
    return render(request, 'pharmacy/profile.html', {
        'orders': orders,
        'prescriptions': prescriptions,
        'orders_count': orders_count,
        'prescriptions_count': prescriptions_count,
        'reviews_count': reviews_count,
        'total_spent': total_spent,
        'recent_orders': recent_orders,
    })

# Wishlist views
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if created:
        messages.success(request, f'{product.name} added to your wishlist!')
    else:
        messages.info(request, f'{product.name} is already in your wishlist!')
    
    return redirect(request.META.get('HTTP_REFERER', 'pharmacy:product_list'))

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        wishlist_item = Wishlist.objects.get(user=request.user, product=product)
        wishlist_item.delete()
        messages.success(request, f'{product.name} removed from your wishlist!')
    except Wishlist.DoesNotExist:
        messages.error(request, 'Product not found in your wishlist!')
    
    return redirect('pharmacy:wishlist')

@login_required
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'pharmacy/wishlist.html', {
        'wishlist_items': wishlist_items
    })

# Enhanced search view
def advanced_search(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort', 'name')
    
    products = Product.objects.filter(is_active=True)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__icontains=query) |
            Q(manufacturer__icontains=query)
        )
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    if min_price:
        products = products.filter(price__gte=min_price)
    
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Sorting
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'rating':
        products = products.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('name')
    
    categories = Category.objects.all()
    
    return render(request, 'pharmacy/advanced_search.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
    })

# Apply coupon view
@login_required
def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code', '').strip().upper()
        
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            
            if not coupon.is_valid():
                messages.error(request, 'This coupon is not valid or has expired.')
            else:
                # Store coupon in session
                request.session['applied_coupon'] = coupon.id
                messages.success(request, f'Coupon {coupon_code} applied successfully!')
                
        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code.')
    
    return redirect('pharmacy:cart')

# Newsletter signup view
def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            messages.success(request, 'Thank you for subscribing to our newsletter!')
        else:
            messages.error(request, 'Please enter a valid email address.')
    return redirect(request.META.get('HTTP_REFERER', 'pharmacy:home'))

# View to handle checkout
@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Your cart is empty!')
        return redirect('pharmacy:cart')
    
    cart_items = []
    subtotal = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            item_total = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total
            })
            subtotal += item_total
        except Product.DoesNotExist:
            continue
    
    # Calculate totals
    tax_rate = 0.18  # 18% GST
    tax_amount = subtotal * tax_rate
    shipping_cost = 50 if subtotal < 500 else 0  # Free shipping above 500
    
    # Apply coupon if exists
    discount_amount = 0
    applied_coupon = None
    coupon_id = request.session.get('applied_coupon')
    
    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            if coupon.is_valid() and subtotal >= coupon.minimum_amount:
                if coupon.discount_type == 'percentage':
                    discount_amount = (subtotal * coupon.discount_value) / 100
                else:
                    discount_amount = coupon.discount_value
                applied_coupon = coupon
        except Coupon.DoesNotExist:
            pass
    
    total_amount = subtotal + tax_amount + shipping_cost - discount_amount
    
    payment_methods = PaymentMethod.objects.filter(is_active=True)
    
    if request.method == 'POST':
        # Process order
        messages.success(request, 'Order placed successfully! You will receive a confirmation email shortly.')
        # Clear cart and coupon
        request.session['cart'] = {}
        if 'applied_coupon' in request.session:
            del request.session['applied_coupon']
        return redirect('pharmacy:profile')
    
    return render(request, 'pharmacy/checkout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'shipping_cost': shipping_cost,
        'discount_amount': discount_amount,
        'total_amount': total_amount,
        'applied_coupon': applied_coupon,
        'payment_methods': payment_methods,
    })