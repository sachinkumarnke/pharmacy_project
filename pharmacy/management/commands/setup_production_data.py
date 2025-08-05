from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from pharmacy.models import Coupon, PaymentMethod

class Command(BaseCommand):
    help = 'Setup production data for pharmacy website'

    def handle(self, *args, **options):
        # Create Payment Methods
        payment_methods = [
            {'name': 'Credit/Debit Card', 'payment_type': 'card', 'icon': 'fas fa-credit-card', 'processing_fee': 0},
            {'name': 'UPI Payment', 'payment_type': 'upi', 'icon': 'fas fa-mobile-alt', 'processing_fee': 0},
            {'name': 'Digital Wallet', 'payment_type': 'wallet', 'icon': 'fas fa-wallet', 'processing_fee': 0},
            {'name': 'Cash on Delivery', 'payment_type': 'cod', 'icon': 'fas fa-money-bill-wave', 'processing_fee': 25},
            {'name': 'Net Banking', 'payment_type': 'bank', 'icon': 'fas fa-university', 'processing_fee': 0},
        ]
        
        for method_data in payment_methods:
            method, created = PaymentMethod.objects.get_or_create(
                name=method_data['name'],
                defaults=method_data
            )
            if created:
                self.stdout.write(f'Created payment method: {method.name}')

        # Create Sample Coupons
        now = timezone.now()
        coupons = [
            {
                'code': 'WELCOME10',
                'discount_type': 'percentage',
                'discount_value': 10,
                'minimum_amount': 100,
                'maximum_uses': 100,
                'valid_from': now,
                'valid_to': now + timedelta(days=30),
            },
            {
                'code': 'SAVE50',
                'discount_type': 'fixed',
                'discount_value': 50,
                'minimum_amount': 500,
                'maximum_uses': 50,
                'valid_from': now,
                'valid_to': now + timedelta(days=15),
            },
            {
                'code': 'HEALTH20',
                'discount_type': 'percentage',
                'discount_value': 20,
                'minimum_amount': 200,
                'maximum_uses': 200,
                'valid_from': now,
                'valid_to': now + timedelta(days=60),
            },
        ]
        
        for coupon_data in coupons:
            coupon, created = Coupon.objects.get_or_create(
                code=coupon_data['code'],
                defaults=coupon_data
            )
            if created:
                self.stdout.write(f'Created coupon: {coupon.code}')

        self.stdout.write(self.style.SUCCESS('Successfully setup production data!'))