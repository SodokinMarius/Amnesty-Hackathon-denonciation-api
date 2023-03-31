# Generated by Django 3.2 on 2023-03-31 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20230331_0957'),
        ('denonciationapp', '0009_notification_sms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='denonciation',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.team'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.team'),
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]
