# Generated by Django 4.2.18 on 2025-02-05 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.CharField(choices=[('birthday', 'Birthday Cakes'), ('wedding', 'Wedding Cakes'), ('cupcake', 'Cupcakes'), ('custom', 'Custom Orders')], max_length=20)),
                ('flavor', models.CharField(blank=True, choices=[('chocolate', 'Chocolate'), ('vanilla', 'Vanilla'), ('red_velvet', 'Red Velvet'), ('lemon', 'Lemon')], max_length=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product_images/')),
                ('available_dates', models.JSONField(default=list, help_text='Available delivery/pickup dates')),
                ('allergen_info', models.TextField(blank=True, help_text='E.g., Contains nuts, gluten-free')),
                ('available', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('rating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='products.product')),
            ],
        ),
    ]
