# Generated manually for production features
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pharmacy', '0009_banner_link_url_banner_photo_alter_banner_icon'),
    ]

    operations = [
        # Add Coupon model
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('discount_type', models.CharField(choices=[('percentage', 'Percentage'), ('fixed', 'Fixed Amount')], max_length=20)),
                ('discount_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('minimum_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('maximum_uses', models.PositiveIntegerField(default=1)),
                ('used_count', models.PositiveIntegerField(default=0)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        
        # Add PaymentMethod model
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('payment_type', models.CharField(choices=[('card', 'Credit/Debit Card'), ('upi', 'UPI'), ('wallet', 'Digital Wallet'), ('cod', 'Cash on Delivery'), ('bank', 'Net Banking')], max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('processing_fee', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('icon', models.CharField(blank=True, max_length=50)),
            ],
        ),
        
        # Add Wishlist model
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'product')},
            },
        ),
    ]