from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from .models import AdvUser
from .models import user_registrated
from .models import Reservation
from .models import Room

import calendar
from datetime import datetime, timedelta

class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True,
        label='Адрес электронной почты')

    class Meta:
        model=AdvUser
        fields=('username', 'email', 'first_name', 'last_name')

class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput,
                                help_text= mark_safe("""<ul><li>Пароль не должен быть слишком похож на другую личную информацию</li>
                                                     <li>Пароль должен содержать как минимум 8 символов</li>
                                                     <li>Пароль не может состоять полностью из цифр</li></ul>""") 
                                          )
    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput,
                                help_text='Пароли должны совпадать')
    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                'Введённые пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registrated.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name',
                  'password1', 'password2')

def calendar_choices(this_date):
    month_range = calendar.monthrange(this_date.year, this_date.month)
    max_day = month_range[1]      #последний день месяца
    days = []
    for day_count in range(max_day):
        if day_count + 1 >= this_date.day:
            str_day = str(day_count + 1) + '.' + str(this_date.month) + '.' + str(this_date.year)
            days.append((str_day, day_count + 1))
    return days

def get_list_time(name_time):

    label_times = ('8', '', '9', '', '10', '', '11', '', '12', '', '13', '', '14', '',
                   '15', '', '16', '', '17', '', '18', '', '19', '', '20', '', '21', '',)

    begin_value = ('08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
                   '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30',
                   '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30',
                   '20:00', '20:30', '21:00', '21:30',)

    end_value = ('08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00',
                 '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00',
                 '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00',
                 '20:30', '21:00', '21:30', '22:00')

    list_time = []
    value = []

    if name_time == 'time_begin':
        value = begin_value
    elif name_time == 'time_end':
        value = end_value

    for i in range(len(value)):
            list_time.append((value[i], label_times[i]))
    return list_time

class UserReservationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserReservationForm, self).__init__(*args, **kwargs)
        self.fields['room'].initial = 1                         # по умолчанию первая комната
        self.fields['room'].empty_label = None                  # выбора пустого варианта нет

    class Meta:
        model = Reservation
        fields = '__all__'

        list_day = []                   # список дней
        this_date = datetime.today()    # текущая дата

        for i in range(3):
            list_day += calendar_choices(this_date)                                     # прибавляем дни
            quantity_days = calendar.monthrange(this_date.year, this_date.month)[1]     # кол-во дней в месяце
            delta_days = quantity_days - this_date.day + 1                              # дней до конца месяца
            this_date = this_date + timedelta(days=delta_days)          # меняем дату на 1 число следующего месяца

        widgets = {'user_id': forms.HiddenInput,
                   'day': forms.RadioSelect(attrs={'name': 'number_day', 'onchange': 'change_day(this)'},
                                            choices=list_day),
                   'time_begin': forms.RadioSelect(attrs={'onclick': 'change_time_begin(this)', 'disabled': 'True'},
                                                   choices=get_list_time('time_begin')),
                   'time_end': forms.RadioSelect(attrs={'onclick': 'change_time_end(this)'},
                                                 choices=get_list_time('time_end')),
                   'room': forms.Select(attrs={'id': 'room_selector', 'class': 'select_room',
                                               'onchange': 'select_room(this)'}),
                   }
