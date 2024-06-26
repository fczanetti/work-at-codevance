# Generated by Django 5.0.6 on 2024-05-16 19:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('payments', '0010_alter_anticipation_creation_date_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='anticipation',
            name='new_value',
            field=models.FloatField(verbose_name='New value'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='creation_date',
            field=models.DateField(auto_now_add=True, verbose_name='Registered in'),
        ),
        migrations.AlterField(
            model_name='requestlog',
            name='action',
            field=models.CharField(choices=[('A', 'Approval'), ('D', 'Denial'), ('R', 'Request')], max_length=8,
                                   verbose_name='Action'),
        ),
        migrations.AlterField(
            model_name='requestlog',
            name='anticipation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.anticipation',
                                    verbose_name='Anticipation'),
        ),
        migrations.AlterField(
            model_name='requestlog',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Registered in'),
        ),
        migrations.AlterField(
            model_name='requestlog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                    verbose_name='User'),
        ),
    ]
