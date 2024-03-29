# Generated by Django 5.0.1 on 2024-01-19 10:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apostilas', '0002_viewapostila'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvaliacaoApostila',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avaliacao', models.CharField(choices=[('B', 'Bom'), ('R', 'Ruim'), ('P', 'Pode Melhorar')], max_length=1)),
                ('apostila', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='apostilas.apostila')),
            ],
        ),
    ]
