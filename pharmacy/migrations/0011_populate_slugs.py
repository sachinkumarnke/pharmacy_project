# Generated manually to populate slugs before adding unique constraint
from django.db import migrations, models
from django.utils.text import slugify


def populate_slugs(apps, schema_editor):
    Product = apps.get_model('pharmacy', 'Product')
    for product in Product.objects.all():
        if not hasattr(product, 'slug') or not product.slug:
            base_slug = slugify(product.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            product.slug = slug
            product.save()


def reverse_populate_slugs(apps, schema_editor):
    pass  # No reverse operation needed


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0010_production_features'),
    ]

    operations = [
        # First add slug field without unique constraint
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        # Populate slugs
        migrations.RunPython(populate_slugs, reverse_populate_slugs),
        # Then make it unique
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]