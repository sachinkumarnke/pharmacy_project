# Generated manually to add order_number field

from django.db import migrations, models
import uuid

def generate_order_numbers(apps, schema_editor):
    Order = apps.get_model('pharmacy', 'Order')
    for order in Order.objects.all():
        if not order.order_number:
            order.order_number = f"ORD{uuid.uuid4().hex[:8].upper()}"
            order.save()

class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0015_add_timestamp_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_number',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.RunPython(generate_order_numbers),
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]