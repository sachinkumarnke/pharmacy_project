from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0005_productimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('license_number', models.CharField(max_length=50, unique=True)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('hospital', models.CharField(blank=True, max_length=200)),
                ('experience_years', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('specialization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy.specialization')),
            ],
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='product',
        ),
        migrations.RemoveField(
            model_name='prescription',
            name='approved',
        ),
        migrations.AddField(
            model_name='prescription',
            name='patient_name',
            field=models.CharField(default='Unknown Patient', max_length=200),
        ),
        migrations.AddField(
            model_name='prescription',
            name='patient_phone',
            field=models.CharField(default='0000000000', max_length=15),
        ),
        migrations.AddField(
            model_name='prescription',
            name='patient_email',
            field=models.EmailField(default='patient@example.com', max_length=254),
        ),
        migrations.AddField(
            model_name='prescription',
            name='doctor_name',
            field=models.CharField(default='Unknown Doctor', help_text='Doctor name from prescription', max_length=200),
        ),
        migrations.AddField(
            model_name='prescription',
            name='delivery_address',
            field=models.TextField(default='Address not provided'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='special_instructions',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='prescription',
            name='is_urgent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='prescription',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending Review'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('fulfilled', 'Fulfilled')], default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='prescription',
            name='reviewed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='prescription',
            name='notes',
            field=models.TextField(blank=True, help_text='Admin notes'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pharmacy.doctor'),
        ),
        migrations.AddField(
            model_name='prescription',
            name='reviewed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_prescriptions', to='auth.user'),
        ),
    ]