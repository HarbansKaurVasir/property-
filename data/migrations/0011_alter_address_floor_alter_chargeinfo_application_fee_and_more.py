# Generated by Django 5.0.3 on 2024-03-15 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0010_documentinfo_documents_property_document_info_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='floor',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='chargeinfo',
            name='application_fee',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='chargeinfo',
            name='broker_fee',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='chargeinfo',
            name='extra_fee_cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='chargeinfo',
            name='first_month_rent',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='chargeinfo',
            name='security_deposit',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='economicinfo',
            name='cost',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='economicinfo',
            name='updated_cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='extrafee',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='generalinfo',
            name='floor',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='generalinfo',
            name='unit',
            field=models.CharField(max_length=10),
        ),
    ]
