from django.core.management.base import BaseCommand
from pharmacy.models import Category, Product
from django.core.files.base import ContentFile
import requests
from io import BytesIO

class Command(BaseCommand):
    help = 'Create sample products with images'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Pain Relief', 'description': 'Medications for pain management'},
            {'name': 'Vitamins', 'description': 'Essential vitamins and supplements'},
            {'name': 'Cold & Flu', 'description': 'Cold and flu medications'},
            {'name': 'First Aid', 'description': 'First aid supplies and equipment'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Sample products data
        products_data = [
            {
                'name': 'Aspirin 325mg',
                'category': 'Pain Relief',
                'description': 'Fast-acting pain relief for headaches and minor aches',
                'price': 8.99,
                'stock': 50,
                'is_prescription': False,
            },
            {
                'name': 'Vitamin D3 1000 IU',
                'category': 'Vitamins',
                'description': 'Essential vitamin D supplement for bone health',
                'price': 12.99,
                'stock': 30,
                'is_prescription': False,
            },
            {
                'name': 'Cough Syrup',
                'category': 'Cold & Flu',
                'description': 'Effective cough suppressant for dry coughs',
                'price': 15.99,
                'stock': 25,
                'is_prescription': False,
            },
            {
                'name': 'Digital Thermometer',
                'category': 'First Aid',
                'description': 'Accurate digital thermometer for temperature monitoring',
                'price': 19.99,
                'stock': 15,
                'is_prescription': False,
            },
            {
                'name': 'Ibuprofen 200mg',
                'category': 'Pain Relief',
                'description': 'Anti-inflammatory pain reliever',
                'price': 9.99,
                'stock': 40,
                'is_prescription': False,
            },
            {
                'name': 'Multivitamin Complex',
                'category': 'Vitamins',
                'description': 'Complete daily vitamin supplement',
                'price': 24.99,
                'stock': 35,
                'is_prescription': False,
            },
        ]

        # Create products
        for product_data in products_data:
            category = categories[product_data.pop('category')]
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'category': category,
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'stock': product_data['stock'],
                    'is_prescription': product_data['is_prescription'],
                }
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')

        self.stdout.write(self.style.SUCCESS('Successfully created sample products!'))
        self.stdout.write('You can now upload images through Django admin at /admin/')