# Generated manually to add missing Order fields

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0016_add_order_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(max_length=20, default='pending'),
        ),
        migrations.AddField(
            model_name='order',
            name='subtotal',
            field=models.DecimalField(max_digits=10, decimal_places=2, default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=15, default=''),
        ),
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default='customer@example.com'),
        ),
        migrations.AddField(
            model_name='order',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]