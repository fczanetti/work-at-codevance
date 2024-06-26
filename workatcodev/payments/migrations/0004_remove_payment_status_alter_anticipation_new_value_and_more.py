# Generated by Django 5.0.4 on 2024-05-06 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_alter_payment_value_anticipation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='status',
        ),
        migrations.AlterField(
            model_name='anticipation',
            name='new_value',
            field=models.FloatField(editable=False, verbose_name='Valor com desconto'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='value',
            field=models.FloatField(verbose_name='Valor'),
        ),
    ]
