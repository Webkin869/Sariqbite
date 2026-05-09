from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('slug', models.SlugField(unique=True)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(blank=True, max_length=30)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True)),
                ('image_url', models.URLField(blank=True)),
                ('sort_order', models.PositiveIntegerField(default=0)),
            ],
            options={'verbose_name_plural': 'categories', 'ordering': ['sort_order', 'name']},
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('image_url', models.URLField(blank=True)),
                ('prep_minutes', models.PositiveIntegerField(default=20)),
                ('spice_level', models.PositiveIntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='catalog.category')),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='ProductOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('extra_price', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('is_active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='catalog.product')),
            ],
            options={'ordering': ['name']},
        ),
    ]
