# Generated by Django 4.2.1 on 2023-06-23 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_payment_teacher_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='invoice_number',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
