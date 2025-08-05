# Generated manually to add missing Product fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0012_add_remaining_fields'),
    ]

    operations = [
        # Add all missing Product fields
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='manufacturer',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='product',
            name='short_description',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='product',
            name='mrp',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, help_text='Maximum Retail Price'),
        ),
        migrations.AddField(
            model_name='product',
            name='min_stock_level',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Weight in grams', max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='dimensions',
            field=models.CharField(blank=True, help_text='L x W x H in cm', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='expiry_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='batch_number',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='product',
            name='benefits',
            field=models.TextField(blank=True, help_text='Product benefits'),
        ),
        migrations.AddField(
            model_name='product',
            name='ingredients',
            field=models.TextField(blank=True, help_text='Active ingredients'),
        ),
        migrations.AddField(
            model_name='product',
            name='uses',
            field=models.TextField(blank=True, help_text='What is it used for'),
        ),
        migrations.AddField(
            model_name='product',
            name='side_effects',
            field=models.TextField(blank=True, help_text='Possible side effects'),
        ),
        migrations.AddField(
            model_name='product',
            name='how_to_use',
            field=models.TextField(blank=True, help_text='Usage instructions'),
        ),
        migrations.AddField(
            model_name='product',
            name='precautions',
            field=models.TextField(blank=True, help_text='Precautions and warnings'),
        ),
        migrations.AddField(
            model_name='product',
            name='safety_info',
            field=models.TextField(blank=True, help_text='Safety information'),
        ),
        migrations.AddField(
            model_name='product',
            name='storage_instructions',
            field=models.TextField(blank=True, help_text='How to store the medicine'),
        ),
    ]