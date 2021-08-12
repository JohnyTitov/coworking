from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal

from .utilities import send_activation_notification

user_registrated = Signal(providing_args=['instance'])


def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_registrated.connect(user_registrated_dispatcher)


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True,
                                       verbose_name='Прошёл активацию?')

    class Meta(AbstractUser.Meta):
        pass


class Room(models.Model):
    name_room = models.CharField(max_length=100, db_index=True, unique=True, verbose_name='Название помещения')
    price_room = models.PositiveSmallIntegerField(verbose_name='Цена')
    about_room = models.TextField(verbose_name='Информация')
    image_room = models.ImageField(default='default.png', verbose_name='изображение')

    def __str__(self):
        return self.name_room

    class Meta:
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'


class Reservation(models.Model):
    user_id = models.ForeignKey(AdvUser, verbose_name='Пользователь', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, verbose_name='Помещение', null=True, on_delete=models.PROTECT)
    day = models.DateField(verbose_name='День')
    time_begin = models.TimeField(verbose_name='c')
    time_end = models.TimeField(verbose_name='до')

    def __str__(self):
        reserv_name = str(self.room) + ' ' + str(self.day) + ' c ' + str(self.time_begin) + ' по ' + str(self.time_end)
        return reserv_name

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Забронировано'
