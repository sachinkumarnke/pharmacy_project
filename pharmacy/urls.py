from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('prescriptions/', views.prescriptions, name='prescriptions'),
    path('doctors/', views.doctors, name='doctors'),
    path('profile/', views.profile, name='profile'),
    path('auth/', views.auth_view, name='auth'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('decrease_cart/<int:product_id>/', views.decrease_cart, name='decrease_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('advanced_search/', views.advanced_search, name='advanced_search'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
]