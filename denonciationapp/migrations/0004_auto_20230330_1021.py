# Generated by Django 3.2 on 2023-03-30 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('denonciationapp', '0003_denonciator_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='denonciation',
            name='description',
            field=models.TextField(verbose_name='Description de la denonciation'),
        ),
        migrations.AlterField(
            model_name='denonciation',
            name='pictures',
            field=models.ImageField(upload_to='images/denonciations_images'),
        ),
    ]
