from django import template

register = template.Library()


@register.filter(name='index')
def index(List, i):
    return List[int(i)]


@register.filter(name='return_date')
def return_date(list_form_day, day):
    for form_day in list_form_day:
        if form_day.data['value'] == day.value:
            return form_day
    return day.number

@register.filter(name='module_2')
def module_2(a):
    return a % 2 == 0

@register.filter(name='get_label_begin')
def get_label_begin(index):
    begin_label = {0: '08:00', 1: '08:30', 2: '09:00', 3: '09:30', 4: '10:00', 5: '10:30', 6: '11:00', 7: '11:30',
                   8: '12:00', 9: '12:30', 10: '13:00', 11: '13:30', 12: '14:00', 13: '14:30', 14: '15:00',
                   15: '15:30', 16: '16:00', 17: '16:30', 18: '17:00', 19: '17:30', 20: '18:00', 21: '18:30',
                   22: '19:00', 23: '19:30', 24: '20:00', 25: '20:30', 26: '21:00', 27: '21:30', }
    return begin_label[index]

@register.filter(name='get_label_end')
def get_label_end(index):
    end_label = {0: '08:30', 1: '09:00', 2: '09:30', 3: '10:00', 4: '10:30', 5: '11:00', 6: '11:30', 7: '12:00',
                 8: '12:30', 9: '13:00', 10: '13:30', 11: '14:00', 12: '14:30', 13: '15:00', 14: '15:30',
                 15: '16:00', 16: '16:30', 17: '17:00', 18: '17:30', 19: '18:00', 20: '18:30', 21: '19:00',
                 22: '19:30', 23: '20:00', 24: '20:30', 25: '21:00', 26: '21:30', 27: '22:00', }
    return end_label[index]