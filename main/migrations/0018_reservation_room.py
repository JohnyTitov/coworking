# Generated by Django 3.0.3 on 2020-03-15 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20200315_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='main.Room', verbose_name='Помещение'),
        ),
    ]