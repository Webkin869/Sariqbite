from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=120)),
                ('phone', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=255)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('note', models.TextField(blank=True)),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('card', 'Card'), ('click', 'Click'), ('payme', 'Payme')], default='cash', max_length=20)),
                ('status', models.CharField(choices=[('received', 'Received'), ('cooking', 'Cooking'), ('on_the_way', 'On the way'), ('delivered', 'Delivered'), ('canceled', 'Canceled')], default='received', max_length=20)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('delivery_fee', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('distance_km', models.FloatField(default=0)),
                ('eta_minutes', models.PositiveIntegerField(default=25)),
                ('telegram_chat_id', models.CharField(blank=True, max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='catalog.branch')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=140)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('options_text', models.CharField(blank=True, max_length=255)),
                ('line_total', models.DecimalField(decimal_places=2, max_digits=12)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
            ],
        ),
    ]
