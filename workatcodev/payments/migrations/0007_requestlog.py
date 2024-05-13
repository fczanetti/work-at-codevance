# Generated by Django 5.0.4 on 2024-05-13 12:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('payments', '0006_alter_anticipation_new_value'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Registrado em')),
                ('action',
                 models.CharField(choices=[('A', 'Approval'), ('D', 'Denial'), ('R', 'Request')], max_length=8,
                                  verbose_name='Ação')),
                ('anticipation',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.anticipation',
                                   verbose_name='Antecipação')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                           verbose_name='Usuário')),
            ],
        ),
    ]
