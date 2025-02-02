# Generated by Django 5.0.3 on 2024-03-11 09:23

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(max_length=255)),
                ('place_id', models.CharField(default='', max_length=255)),
                ('address_place_id', models.CharField(max_length=255)),
                ('unit_code', models.CharField(default='', max_length=10)),
                ('floor', models.PositiveIntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GeneralInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('unit', models.CharField(default='', max_length=10)),
                ('floor', models.IntegerField(default=2)),
                ('bedrooms', models.CharField(default='', max_length=10)),
                ('bathrooms', models.CharField(default='', max_length=10)),
                ('agent_id', models.CharField(default='', max_length=36)),
                ('apartment_number', models.IntegerField(default=0)),
                ('property_name', models.CharField(default='', max_length=255)),
                ('date_available', models.DateField(default='2024-04-15')),
                ('description', models.TextField(default='')),
                ('is_easy_apply', models.BooleanField(default=False)),
                ('address', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='general_info', to='data.address')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('general_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='property', to='data.generalinfo')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
