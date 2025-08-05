from django.contrib import admin
from django.utils.html import format_html
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from .models import Category, Product, ProductImage, Prescription, Order, OrderItem, Doctor, Specialization, Banner, Coupon, PaymentMethod, Wishlist

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'license_number', 'hospital', 'experience_years', 'photo_preview', 'is_active']
    list_filter = ['specialization', 'is_active', 'experience_years']
    search_fields = ['name', 'license_number', 'hospital']
    list_editable = ['is_active']
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'specialization', 'license_number', 'photo')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'hospital')
        }),
        ('Professional Details', {
            'fields': ('experience_years', 'is_active')
        }),
    )
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%; border: 2px solid #28a745;" />', obj.photo.url)
        return format_html('<div style="width: 50px; height: 50px; background: #f8f9fa; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 2px solid #dee2e6;"><i class="fas fa-user-md" style="color: #6c757d;"></i></div>')
    photo_preview.short_description = 'Photo'

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    max_num = 4
    fields = ['image', 'alt_text', 'is_primary']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_prescription', 'image_preview']
    list_filter = ['category', 'is_prescription', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['price', 'stock']
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description', 'price', 'stock', 'is_prescription', 'image')
        }),
        ('Detailed Information', {
            'fields': ('benefits', 'ingredients', 'uses', 'side_effects', 'how_to_use', 'precautions', 'safety_info'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image'

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'doctor_name', 'status', 'is_urgent', 'uploaded_at', 'image_preview']
    list_filter = ['status', 'is_urgent', 'uploaded_at', 'doctor__specialization']
    list_editable = ['status']
    search_fields = ['patient_name', 'doctor_name', 'patient_email']
    readonly_fields = ['uploaded_at', 'user']
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('user', 'patient_name', 'patient_phone', 'patient_email')
        }),
        ('Doctor Information', {
            'fields': ('doctor', 'doctor_name')
        }),
        ('Prescription Details', {
            'fields': ('image', 'delivery_address', 'special_instructions', 'is_urgent')
        }),
        ('Review Information', {
            'fields': ('status', 'reviewed_by', 'reviewed_at', 'notes'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Prescription'
    
    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            obj.reviewed_by = request.user
            from django.utils import timezone
            obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'total_price', 'is_paid']
    list_filter = ['is_paid', 'created_at']
    inlines = [OrderItemInline]

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'photo_preview', 'icon_preview', 'link_url', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active', 'order']
    search_fields = ['title', 'link_url']
    ordering = ['order', 'created_at']
    
    fieldsets = (
        ('Banner Content', {
            'fields': ('title', 'photo', 'icon')
        }),
        ('Link Settings', {
            'fields': ('link_url',)
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="30" style="object-fit: cover; border-radius: 4px;" />', obj.photo.url)
        return "No Photo"
    photo_preview.short_description = 'Photo'
    
    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<i class="{}"></i> {}', obj.icon, obj.icon)
        return "No Icon"
    icon_preview.short_description = 'Icon'

# Custom admin site configuration
class PharmacyAdminSite(AdminSite):
    site_header = 'AyuRx Pharmacy Administration'
    site_title = 'AyuRx Admin'
    index_title = 'AyuRx Management Dashboard'
    
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({
            'products_count': Product.objects.count(),
            'orders_count': Order.objects.count(),
            'users_count': User.objects.count(),
            'categories_count': Category.objects.count(),
        })
        return super().index(request, extra_context)

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'minimum_amount', 'used_count', 'maximum_uses', 'is_active', 'valid_from', 'valid_to']
    list_filter = ['discount_type', 'is_active', 'valid_from', 'valid_to']
    search_fields = ['code']
    list_editable = ['is_active']
    readonly_fields = ['used_count']

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'payment_type', 'processing_fee', 'is_active']
    list_filter = ['payment_type', 'is_active']
    list_editable = ['is_active', 'processing_fee']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at', 'product__category']
    search_fields = ['user__username', 'product__name']
    readonly_fields = ['created_at']

# Override default admin site
admin.site.__class__ = PharmacyAdminSite