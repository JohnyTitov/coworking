from django.shortcuts import render
from django.contrib.auth.views import LoginView             # Чтобы залогиниться можно было
from django.contrib.auth.decorators import login_required   # просмотр профиля
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.core.signing import BadSignature
from django.views.generic.edit import DeleteView    # чтобы удалять юзеров
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponse

from .models import AdvUser
from .models import Room
from .models import Reservation
from .forms import ChangeUserInfoForm   # форма редактирования пользовательских данных
from .forms import RegisterUserForm     # форма регистрации
from .forms import UserReservationForm
from .utilities import signer           # для отправки email

import calendar
from datetime import datetime, timedelta


def index(request):
    return render(request, 'main/index.html')

def RoomView(request):
    ListRoom = Room.objects.all()
    return render(request, 'main/room.html',{'ListRoom': ListRoom})

def rezervation_validator(form):    # проверка введенных в форму данных
    this_room = form.cleaned_data.get("room")                        # заданная комната
    ListReservation = Reservation.objects.filter(room=this_room)     # список брони заданной комнаты

    form_time_begin = form.cleaned_data.get("time_begin")   # время начала в форме
    form_time_end = form.cleaned_data.get("time_end")       # время конца в форме
    form_day = form.cleaned_data.get("day")                 # дата в форме

    TODAY = datetime.date(datetime.today())                 # сегодняшний день
    TODAY_TIME = datetime.time(datetime.today())            # сколько сейчас времени

    if form_day < TODAY:
        return False, 'Выберите дату начиная с сегодняшнего дня'
    elif form_day == TODAY and form_time_begin < TODAY_TIME:
        return False, 'Нельзя забронировать прошедшее время'
    elif form_time_end <= form_time_begin:
        return False, 'Нельзя забронировать помещение меньше, чем на 30 минут'
    elif form_time_end.minute != 30 and form_time_end.minute != 0:
        return False, 'Поле минуты должно содержать 30 или 00'
    elif form_time_begin.minute != 30 and form_time_begin.minute != 0:
        return False, 'Поле минуты должно содержать 30 или 00'
    elif form_time_begin.hour < 8 or form_time_begin.hour > 22:
        return False, 'Можно бронировать только начиная с 8:00 до 22:00'
    elif form_time_end.hour < 8 or form_time_end.hour > 22:
        return False, 'Можно бронировать только начиная с 8:00 до 22:00'
    else:
        for reservation in ListReservation:
            if form_day == reservation.day:
                if form.cleaned_data.get("user_id") == reservation.user_id:     # если соседнее объявление того же юзера
                    if form_time_begin < reservation.time_end and form_time_end > reservation.time_begin:
                        return False, 'Это время уже занято'
                else:
                    if form_time_begin <= reservation.time_end and form_time_end >= reservation.time_begin:
                        return False, 'Это время уже занято'
        return True, 'Объявление добавлено'

class Calendar_day(object):
    number = ''
    color = None
    value = None
    times = None
    room_id = None

    def __init__(self, month, year):
        self.month = month
        self.year = year

    def set_data_and_times(self, day, this_room, this_user):
        reservation_times = {(8, 0): None, (8, 30): None, (9, 0): None, (9, 30): None,  # словарь с временем
                             (10, 0): None, (10, 30): None, (11, 0): None, (11, 30): None,
                             (12, 0): None, (12, 30): None, (13, 0): None, (13, 30): None,
                             (14, 0): None, (14, 30): None, (15, 0): None, (15, 30): None,
                             (16, 0): None, (16, 30): None, (17, 0): None, (17, 30): None,
                             (18, 0): None, (18, 30): None, (19, 0): None, (19, 30): None,
                             (20, 0): None, (20, 30): None, (21, 0): None, (21, 30): None, }

        string_date = str(self.year) + '-' + str(self.month) + '-' + str(day)
        list_reservation = Reservation.objects.filter(day=string_date,
                                                      room=this_room)  # список брони текущей комнаты на сегодня

        for reservation in list_reservation:
            this_time = {'hour': reservation.time_begin.hour,
                         'minute': reservation.time_begin.minute}  # время, которое в цикле прибавляется

            while (this_time['hour'] * 60 + this_time['minute']) < (
                    reservation.time_end.hour * 60 + reservation.time_end.minute):
                reservation_times[(this_time['hour'], this_time[
                    'minute'])] = reservation.user_id.username  # в словарь по этому времени записываем id данного юзера
                this_time['minute'] += 30
                if this_time['minute'] == 60:
                    this_time['hour'] += 1
                    this_time['minute'] = 0

        time_out = []   # список получасовых перерывов между бронями
        list_time = list(reservation_times.keys())    # список времени
        list_user = list(reservation_times.values())  # список юзеров

        for i in range(len(list_user)):     # добавляем перерывы после занятого времени
            if i != 0:      # если не первый эл-т
                if not list_user[i] and list_user[i-1]:    # если время время не занято, а предыдущее занято
                    if list_user[i-1] != this_user:        # если занято не текущим юзером
                        time_out.append([list_time[i], 'time_out'])     # добавляем это время в тайм аут

        for i in range(len(list_user)):     # добавляем перерывы перед занятым временем
            if i != (len(list_user)-1):     # если не последний эл-т
                if not list_user[i] and list_user[i+1]:    # если время время не занято, а следующее занято
                    if list_user[i+1] != this_user:        # если занято не текущим юзером
                        time_out.append([list_time[i], 'time_out'])     # добавляем это время в тайм аут

        for time in time_out:   # добавляем тайм ауты в список занятого времени
            reservation_times[time[0]] = time[1]

        for time in reservation_times.keys():   # заменяем имена юзеров и None цветами green и red
            if not reservation_times[time]:
                reservation_times[time] = 'green'
            else:
                reservation_times[time] = 'red'

        self.number = day
        self.times = reservation_times
        self.value = str(self.number) + '.' + str(self.month) + '.' + str(self.year)
        self.room_id = this_room.id

    def traffic_light(self):    # функция "светофор"
        count_time = 0  # счетчик занятого времени
        for value in self.times.values():
            if value == 'red':
                count_time += 1
        if count_time == len(self.times):
            self.color = 'red'
        elif count_time == 0:
            self.color = 'green'
        else:
            self.color = 'yellow'

    def color_grey(self):
        self.color = 'grey'

class Calendar_month(object):
    dict_month = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
                  9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'}

    def __init__(self, this_date, current_user):
        self.current_user = current_user        # текущий юзер
        self.this_date = this_date              # текущая дата
        self.name = self.dict_month[this_date.month] + ' ' + str(this_date.year)    # название месяца
        self.list_week = self.calendar_view()   # список недель
        self.number = None                      # номер месяца (1, 2 или 3)

    def put_number_month(self, number):
        self.number = number

    def calendar_view(self):   # формирует календарик
        month_range = calendar.monthrange(self.this_date.year, self.this_date.month)

        weeks = []                          # список списков недель для каждой комнаты
        list_room = Room.objects.all()      # список комнат
        for room in list_room:
            week_one_day = month_range[0]   # день недели первого дня месяца
            max_day = month_range[1]        # последний день месяца
            day_count = 0                   # счетчик дней
            list_week = []                  # список недель для данной комнаты
            for week in range(6):
                list_day = []               # список дней
                for week_day in range(7):
                    day = Calendar_day(self.this_date.month, self.this_date.year)        # создаём день
                    if week_one_day > week_day:     # если (день недели 1-го дня месяца) > (текущего дня недели)
                        day.color_grey()            # день не существует
                    else:
                        week_one_day = 0
                        day_count += 1
                        if day_count > max_day:     # если (текущий день) > (последнего дня месяца)
                            day.color_grey()        # то день не существует
                        else:
                            day.set_data_and_times(day_count, room, self.current_user)     # присваиваем дню число и список времени
                            if day.number < self.this_date.day:         # (текущий день) < сегодня
                                day.color_grey()                        # день не активен
                            else:
                                day.traffic_light()                     # зелёный, жёлтый или красный
                    list_day.append(day)            # прибавляем день
                list_week.append(list_day)          # прибавляем неделю
            weeks.append(list_week)                 # прибавляем список недель для данной комнаты
        return weeks


@login_required
def reservation(request):  # для бронирования
    this_date = datetime.today()            # текущая дата
    list_month = []                         # список месяцев
    current_user = request.user.username    # текущий юзер

    for i in range(3):
        this_month = Calendar_month(this_date, current_user)                        # создаём месяц
        list_month.append(this_month)                                               # добавляем месяц в список
        quantity_days = calendar.monthrange(this_date.year, this_date.month)[1]     # кол-во дней в месяце
        delta_days = quantity_days - this_date.day +1                               # дней до конца месяца
        this_date = this_date + timedelta(days=delta_days)                  # меняем дату на 1 число следующего месяца

    for i in range(len(list_month)):
        list_month[i].put_number_month(i)

    if request.method == 'POST':
        form = UserReservationForm(request.POST)
        if form.is_valid():
            valid = rezervation_validator(form)
            if valid[0]:
                form.save()
                messages.add_message(request, messages.SUCCESS, valid[1])
            else:
                messages.add_message(request, messages.ERROR, valid[1])
    else:
        form = UserReservationForm(initial={'user_id': request.user.pk})
    context = {'form': form, 'list_month': list_month}
    return render(request, 'main/reservation.html', context)

class BBLoginView(LoginView):
    template_name='main/login.html'

class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin,
                         UpdateView):
    model = AdvUser
    template_name = 'main/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile_change')
    success_message = 'личные данные пользователя изменены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk = self.user_id)

class PasswordChangeView(SuccessMessageMixin, LoginRequiredMixin,
                             PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('main:profile_change')
    success_message = "Пароль успешно изменён"

class RegisterUserView(CreateView): #контроллер регистрации
    model = AdvUser
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')

class RegisterDoneView(TemplateView):   #контроллер уведомляющий о регистрации
    template_name = 'main/register_done.html'

def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)

class DeleteuserView (LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('main:index')

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удалён')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
