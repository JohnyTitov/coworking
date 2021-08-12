from django.contrib import admin
import datetime

from .models import AdvUser
from .models import Room
from .models import Reservation
from .utilities import send_activation_notification

def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Письма с оповещениями отправлены')

send_activation_notifications.short_description = 'отправка писем с' +\
'оповещениями об активации'

class NonactivatedFilter(admin.SimpleListFilter):
    title = ''
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated','Прошедшие активацию'),
            ('noactiv','Непрошедшие'),
            )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'noactiv':
            return queryset.filter(is_active=False, is_activated=False) 


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__','first_name', 'last_name','email','is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonactivatedFilter,)
    fields = (('username', 'email'),('first_name', 'last_name'),
              ('is_active','is_activated'),
              ('is_staff', 'is_superuser'),
              'groups', 'user_permissions',
              ('last_login', 'date_joined'))
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications,)



class AdminRoom(admin.ModelAdmin):
    model = Room
    search_fields=('name_room',)
    list_display = ('name_room', 'price_room')

class AdminReservation(admin.ModelAdmin):
    model = Reservation
    search_fields = ('user_id',)
    list_display = ('user_id', 'room', 'day', 'time_begin', 'time_end')
    ordering = ('-day','-time_begin',)
admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(Room,AdminRoom)
admin.site.register(Reservation,AdminReservation )