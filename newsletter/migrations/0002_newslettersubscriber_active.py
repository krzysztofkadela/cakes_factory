# Generated by Django 4.2.18 on 2025-03-16 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newslettersubscriber',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
