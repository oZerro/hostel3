from django.contrib import admin

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
    Contact,
)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email']
    list_editable = []


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['number', 'price_for_period', 'number_of_beds']
    list_editable = ['price_for_period', 'number_of_beds']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['date', 'name', 'phone_number', 'room']
    list_editable = ['room']

@admin.register(Departures)
class DeparturesAdmin(admin.ModelAdmin):
    list_display = ['date', 'user', 'phone_number']
    list_editable = []


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'date', 'method', 'summa']
    list_editable = []


@admin.register(Refunds)
class RefundsAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'method', 'summa']
    list_editable = []


@admin.register(SpendingAdmin)
class SpendingAdmin(admin.ModelAdmin):
    list_display = ['date', 'summa', 'note']
    list_editable = ['summa', 'note']


@admin.register(SpendingHostel)
class SpendingHostelAdmin(admin.ModelAdmin):
    list_display = ['date', 'summa', 'note']
    list_editable = ['summa', 'note']


@admin.register(SpendingBoss)
class SpendingBossAdmin(admin.ModelAdmin):
    list_display = ['date', 'summa', 'note']
    list_editable = ['summa', 'note']


@admin.register(Event_plan)
class EventsAdmin(admin.ModelAdmin):
    list_display = ['date', 'event']
    list_editable = ['event']


@admin.register(Event_done)
class EventsAdmin_done(admin.ModelAdmin):
    list_display = ['date', 'event']
    list_editable = ['event']







# Register your models here.
