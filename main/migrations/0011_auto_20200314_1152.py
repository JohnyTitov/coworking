# Generated by Django 3.0.3 on 2020-03-14 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_room_image_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='image_room',
            field=models.ImageField(default='default.png', upload_to='', verbose_name='изображение'),
        ),
    ]
