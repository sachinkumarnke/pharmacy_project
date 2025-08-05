# Generated manually to add missing UserProfile fields

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0017_add_missing_order_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='date_of_birth',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='city',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='state',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='zip_code',
            field=models.CharField(max_length=10, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='country',
            field=models.CharField(max_length=50, default='India'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='newsletter',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='sms_notifications',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email_notifications',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='loyalty_points',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='preferred_language',
            field=models.CharField(max_length=10, default='en'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='emergency_contact',
            field=models.CharField(max_length=15, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='medical_conditions',
            field=models.TextField(blank=True, help_text='Known allergies or medical conditions'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]