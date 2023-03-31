# Generated by Django 3.2 on 2023-03-31 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_administrator_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name="Description de l'Equipe")),
                ('contact', models.TextField(verbose_name="contact de l'Equipe")),
                ('whatsapp', models.TextField(verbose_name="Numéro whatsapp de l'Equipe")),
                ('address', models.JSONField(verbose_name='Localisation')),
            ],
        ),
        migrations.AddField(
            model_name='administrator',
            name='is_team_responsable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='administrator',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.team'),
        ),
    ]
