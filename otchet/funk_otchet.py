from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render
from django.core.mail import send_mail
import datetime

from otchet.models import (
    Profile,
    Room,
    Departures,
    Payments,
    Refunds,
    SpendingAdmin,
    SpendingBoss,
    SpendingHostel,
    Event_plan,
    Event_done,
)
from otchet.forms import (
    InfoUserForm,
    UserLoginForm,
    UserRegisterForm,
    AddPepForm,
    DepartmentForm,
    AddPaymentsForm,
    AddSpendingAdminForm,
    AddSpendingHostelForms,
    AddSpendingBossForms,
    AddEventsForms,
    AddRefundsForms,
    AddRoomForm,
)



def send(user_email, name):
    send_mail(
        'Здарова',
        f'Здарова, {name}',
        'leha.normatov@mail.ru',
        [user_email, ],
        fail_silently=False,
    )


def data_d(request) -> dict:
    data = {}
    if request.user.is_authenticated and request.user.is_staff:
        name = request.user.first_name
        surname = request.user.last_name
        payments = list(Payments.objects.all())[:5]
        data = {
            'name': name,
            'surname': surname,
            'payments': payments
        }

    elif request.user.is_authenticated:
        name = request.user.first_name
        surname = request.user.last_name
        data = {
            'name': name,
            'surname': surname
        }

    data['form'] = AddPepForm()
    data['form1'] = AddPaymentsForm()
    data['form2'] = AddSpendingAdminForm()
    data['form3'] = AddSpendingHostelForms()
    data['form4'] = AddSpendingBossForms()
    data['form5'] = AddEventsForms()
    data['form6'] = AddRefundsForms()
    data['form7'] = DepartmentForm()
    data['form8'] = AddRoomForm()

    return data


def add_paginator(request, obj_model) -> dict:
    data = data_d(request)
    objects_all = obj_model.objects.all()
    paginator = Paginator(objects_all, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data['page_obj'] = page_obj

    return data

def summ_room(number) -> str:
    arr_suum = []
    for pay in Payments.objects.all():
        if (
                int(pay.room) == number and
                datetime.datetime.now().month == pay.date.month
        ):
            arr_suum.append(pay.summa)
    return point_in_number(sum(arr_suum))

def point_in_number(arr) -> str:  # расставляет точки в больших числах
    if arr < 0:
        s = list(str(arr)[1:])
    else:
        s = list(str(arr))

    count = 0
    i = 0
    while i < len(s) - 1:
        count += 1
        i += 1
        if count == 3:
            s.insert(len(s) - i, '.')
            count = 0
            i += 1
    if arr < 0:
        return "-" + "".join(s)
    else:
        return "".join(s)

def suum_vsego() -> tuple:
    arr_suum = []
    for pay in Payments.objects.all():
        if datetime.datetime.now().month == pay.date.month:
            arr_suum.append(pay.summa)
    summa = sum(arr_suum)

    return point_in_number(summa), sum(arr_suum)


def spend_vsego(r) -> tuple:
    arr_suum = []
    for pay in r.objects.all():
        if datetime.datetime.now().month == pay.date.month:
            arr_suum.append(pay.summa)
    summa = sum(arr_suum)

    return point_in_number(summa), sum(arr_suum)


def spending_for_month(s) -> list:
    arr_spend = []
    for pay in s.objects.all():
        if datetime.datetime.now().month == pay.date.month:
            arr_spend.append(pay)
    return arr_spend


def dict_from_list_room(arrivals) -> dict:
    new_people_room = {}
    while len(arrivals) > 0:
        com = arrivals[0]
        x = arrivals.count(com)
        new_people_room[com] = x
        if x > 0:
            while x > 0:
                arrivals.remove(com)
                x -= 1

    return new_people_room


def count_new_people() -> tuple:
    summ = 0 # общая сумма новых людей

    arrivals = []  # заезды
    for profile in Profile.objects.all():
        if profile.date.month == datetime.datetime.now().month:
            if profile.room:
                arrivals.append(profile.room.number)

    for people in Profile.objects.all():
        if datetime.datetime.now().month == people.date.month:
            summ += 1

    if summ:
        return summ, dict_from_list_room(arrivals)
    else:
        return summ, "Без заездов"

def count_old_resident():
    summ = 0  # общая сумма старых жильцов, которые живут больше месяца

    arrivals = []  # список комнат которые живут более месяца
    for profile in Profile.objects.all():
        if profile.date.month < datetime.datetime.now().month:
            if profile.room:
                arrivals.append(profile.room.number)

    for people in Profile.objects.all():
        if datetime.datetime.now().month > people.date.month:
            summ += 1

    if summ:
        return summ, dict_from_list_room(arrivals)
    else:
        return summ, 'Не жили'


def arrivals_departures() -> tuple:
    summ = 0

    arrivals = []  # выезды
    for profile in Departures.objects.all():
        if profile.date.month == datetime.datetime.now().month:
            arrivals.append(profile.room)

    for people in Departures.objects.all():
        if datetime.datetime.now().month == people.date.month:
            summ += 1

    if summ:
        return summ, dict_from_list_room(arrivals)
    else:
        return summ, "Без выездов"

def add_refaunds(form) -> None:
    if form.cleaned_data['summa'] > 0:
        pay = Payments(
            user=form.cleaned_data['user'],
            method=form.cleaned_data['method'],
            name=form.cleaned_data['user'].name,
            summa=form.cleaned_data['summa'] * (-1),
            room=form.cleaned_data['user'].room.number
        )
        pay.save()

        refa = Refunds(
            user=form.cleaned_data['user'],
            method=form.cleaned_data['method'],
            name=form.cleaned_data['user'].name,
            summa=form.cleaned_data['summa'] * (-1),
            room=form.cleaned_data['user'].room.number
        )
        refa.save()
    else:
        pay = Payments(
            user=form.cleaned_data['user'],
            method=form.cleaned_data['method'],
            name=form.cleaned_data['user'].name,
             summa=form.cleaned_data['summa'],
            room=form.cleaned_data['user'].room.number
        )
        pay.save()

        refa = Refunds(
            user=form.cleaned_data['user'],
            method=form.cleaned_data['method'],
            name=form.cleaned_data['user'].name,
            summa=form.cleaned_data['summa'],
            room=form.cleaned_data['user'].room.number
        )
        refa.save()


def add_payments(form) -> bool:
    pay = Payments(
        user=form.cleaned_data['user'],
        method=form.cleaned_data['method'],
        name=form.cleaned_data['user'].name,
        summa=form.cleaned_data['summa'],
        room=form.cleaned_data['user'].room.number

    )
    pay.save()

    return True


def add_customer(form) -> bool:
    if form.cleaned_data['room'].is_full:
        return False
    else:
        profile = Profile(
            name=form.cleaned_data['name'],
            phone_number=form.cleaned_data['phone_number'],
            room=form.cleaned_data['room'],
            room_number=form.cleaned_data['room'].number
        )
        profile.save()
        return True


def add_department(form) -> bool:
    if form.is_valid():
        user_id = form.cleaned_data['user'].id
        user_none = Profile.objects.get(id=user_id)
        depart = Departures(
            name=form.cleaned_data['user'].name,
            phone_number=form.cleaned_data['user'].phone_number,
            room=form.cleaned_data['user'].room.number
        )
        user_none.delete()
        depart.save()
    return True

def count_month_number() -> str:
    if datetime.datetime.now().month < 10:
        month_now = '0' + str(datetime.datetime.now().month)
    else:
        month_now = datetime.datetime.now().month

    return str(month_now)


def otchet_first_block(request) -> str:
    info_otchet = otchet_data(request)
    money_by_room = (
        f"Выручка с 01.{info_otchet['month_now']} по 01.{info_otchet['month_next']}\n\n"
        f"#2 - {info_otchet['summ_2_room']}р\n"
        f"#3 - {info_otchet['summ_3_room']}р\n"
        f"#4 - {info_otchet['summ_4_room']}р\n"
        f"#5 - {info_otchet['summ_5_room']}р\n"
        f"#6 - {info_otchet['summ_6_room']}р\n"
        f"#7 - Кухня\n"
        f"#8 - Столовая\n"
        f"#9 - Котельная\n"
        f"#10 - {info_otchet['summ_10_room']}р\n"
        f"#11 - {info_otchet['summ_11_room']}р\n"
        f"#12 - {info_otchet['summ_12_room']}р\n"
        f"#13 - {info_otchet['summ_13_room']}р\n"
        f"#14 - {info_otchet['summ_14_room']}р\n"
        f"#15 - {info_otchet['summ_15_room']}р\n"
        f"#16 - {info_otchet['summ_16_room']}р\n"
        f"#17 - {info_otchet['summ_17_room']}р\n\n"
        f"ИТОГО:  {info_otchet['suum_vsego']}р\n"
        f"-------------------------------------"
    )

    return money_by_room


def otchet_second_block(request) -> str:
    info_otchet = otchet_data(request)
    spending = "Затраты Бос \n\n"

    if len(info_otchet['spending_boss']) > 0:
        for spend in info_otchet['spending_boss']:
            spending += (f'{spend.date.day}.{spend.date.month}.{spend.date.year} | ' 
                         f' {spend.note} | {spend.summa}р\n')
        spending += "\n"
    else:
        spending += "Затрат не было\n\n"

    spending += f"ИТОГО: {info_otchet['spend_vsego_boss']}р\n"
    spending += "-------------------------------------\n"
    spending += "Затраты Дом \n\n"

    if len(info_otchet['spending_dom']) > 0:
        for spend in info_otchet['spending_dom']:
            spending += (f'{spend.date.day}.{spend.date.month}.{spend.date.year} | ' 
                         f' {spend.note} | {spend.summa}р\n')
        spending += "\n"
    else:
        spending += "Затрат не было\n\n"

    spending += f"ИТОГО: {info_otchet['spend_vsego_dom']}р\n"
    spending += "-------------------------------------"

    return spending


def otchet_third_block(request):
    info_otchet = otchet_data(request)
    old_people = info_otchet['count_old_rezident']
    new_people = info_otchet['count_new_people']
    depart = info_otchet['count_depart_people']

    spending = "Заезды/Выезды \n\n"

    for room in range(2, 18):
        if room in (7, 8, 9):
            if room == 7:
                spending += "#7 - Кухня\n"
            elif room == 8:
                spending += "#8 - Столовая\n"
            else:
                spending += "#9 - Котельная\n"
            continue

        if type(old_people[1]) == str:
            rez1 = old_people[1]
        else:
            rez1 = old_people[1].get(room,) + 'живут'

        if type(new_people[1]) == str:
            rez2 = new_people[1]
        else:
            rez2 = new_people[1].get(room, 'Без заездов')
            if str(rez2).isdigit():
                rez2 = f'+{rez2} чел'

        if type(depart[1]) == str:
            rez3 = depart[1]
        else:
            rez3 = depart[1].get(str(room), 'Без выездов')
            if str(rez3).isdigit():
                rez3 = f'-{rez3} чел'

        spending += (f"#{room}  "
                     f"{rez1} | " 
                     f"{rez2} | "
                     f"{rez3}\n"
                     )
    spending += (
        f'\nИТОГО: {old_people[0]} старых жителей | {new_people[0]} заехали |'  
        f'{depart[0]} съехали \n'
        f'ВСЕГО ЛЮДЕЙ: {old_people[0] + new_people[0]} чел.\n'
        f'-------------------------------------'
        )

    return spending


def four_block_otchet(request):
    info_otchet = otchet_data(request)

    spending = "Мероприятия проведены \n\n"

    if len(info_otchet.get('events')):
        for spend in info_otchet.get('events'):
            spending += (f'{spend.date.day}.{spend.date.month}.{spend.date.year} |'
                         f'{spend.event} \n')
    else:
        spending += "Мероприятий не было \n"

    spending += "-------------------------------------"

    return spending


def five_block_otchet(request):
    info_otchet = otchet_data(request)

    spending = "ИТОГО: \n\n"

    spending += (f'{info_otchet.get("suum_vsego")}р - (выручка)\n'
                 f'-{info_otchet.get("spend_vsego_boss")}р - (затраты босс)\n'
                 f'-{info_otchet.get("spend_vsego_dom")}р - (затраты дом)\n'
                 f'-{info_otchet.get("spend_admin")}р - (аванс админ)\n'
                 f'{info_otchet.get("banca")}р - (остаток на руках)'
                 )
    return spending


def send_otchet(request):
    send_mail(
        subject='Актуальный отчет',
        message=(
            # первый блок отчета - доход по каждой комнате и общий доход
            f'{otchet_first_block(request)}\n'
            # второй блок отчета - показаны затраты 
            f'{otchet_second_block(request)}\n'
            # третий блок - заезды выезды
            f'{otchet_third_block(request)}\n'
            # четвертый блок мероприятия
            f'{four_block_otchet(request)}\n'
            f'Запланированные мероприятия \n\n'
            f'-------------------------------------\n'
            # пятный блок итог
            f'{five_block_otchet(request)}'


        ),
        from_email='leha.normatov@mail.ru',
        recipient_list=['denjll98@mail.ru', 'aa_dimidrol@mail.ru'],
    )


def otchet_data(request) -> dict:
    data = data_d(request)

    month_next = int(count_month_number()) + 1

    data['month_now'] = count_month_number()
    data['month_next'] = month_next

    data['summ_2_room'] = summ_room(2)
    data['summ_3_room'] = summ_room(3)
    data['summ_4_room'] = summ_room(4)
    data['summ_5_room'] = summ_room(5)
    data['summ_6_room'] = summ_room(6)
    data['summ_10_room'] = summ_room(10)
    data['summ_11_room'] = summ_room(11)
    data['summ_12_room'] = summ_room(12)
    data['summ_13_room'] = summ_room(13)
    data['summ_14_room'] = summ_room(14)
    data['summ_15_room'] = summ_room(15)
    data['summ_16_room'] = summ_room(16)
    data['summ_17_room'] = summ_room(17)
    data['suum_vsego'] = suum_vsego()[0]
    data['spending_boss'] = spending_for_month(SpendingBoss)
    data['spend_vsego_boss'] = spend_vsego(SpendingBoss)[0]
    data['spending_dom'] = spending_for_month(SpendingHostel)
    data['spend_vsego_dom'] = spend_vsego(SpendingHostel)[0]
    data['count_old_rezident'] = count_old_resident()
    data['count_new_people'] = count_new_people()
    data['count_depart_people'] = arrivals_departures()
    data['events'] = list(Event_plan.objects.all())
    data['spend_admin'] = spend_vsego(SpendingAdmin)[0]
    data['banca'] = point_in_number((
            suum_vsego()[1] -
            (
                    spend_vsego(SpendingBoss)[1] +
                    spend_vsego(SpendingHostel)[1] +
                    spend_vsego(SpendingAdmin)[1]
            )
    ))

    return data



