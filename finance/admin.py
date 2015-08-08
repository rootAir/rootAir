#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin
from utils.sync_report import *
from django.contrib import messages, admin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic.base import RedirectView
from django import http
from finance.extract import Extract
from finance.provider import Provider
from finance.type_launch import TypeLaunch
from finance.week_number import WeekNumber
from activity.type_activity import TypeActivity
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from utils.util import *
from finance.prevision import *
import random, os
from tasks import *
import datetime
import time
# from django.http import HttpResponsePermanentRedirect
from utils.graphic import *
from finance.contato import *


class FinanceAdmin(admin.ModelAdmin):
    def sync(self, instance):
        """
        :param instance:
        :return:
        """
        return get_synchronized(instance.synchronized)

    sync.short_description = "synchronized"
    sync.allow_tags = True

    def get_readonly_fields(self, request, obj=None):
        """
        :param request:
        :param obj:
        :return:
        """
        if obj:
            return self.readonly_fields + ('synchronized',)
        return self.readonly_fields

    def make_published(modeladmin, request, queryset):
        """
        :param modeladmin:
        :param request:
        :param queryset:
        :return:
        """
        queryset.update(status='p')


class ProviderInline(admin.TabularInline):
    model = Provider
    raw_id_fields = ('type_launch', )


class TypeActivityInline(admin.TabularInline):
    model = TypeActivity


class ExtractAdmin(FinanceAdmin):
    search_fields = ('date_launch', 'launch',)
    list_display = ('id', 'date_launch', 'launch', 'description', 'date_purchase', 'value_debit', 'value_credit', 'value_balance', 'sync')
    list_display_links = ('id', 'date_launch', 'description', 'launch', 'date_purchase' )
    raw_id_fields = ('provider', )
    ordering = ('-date_purchase',)

    def description(self, instance):
        """
        :param instance:
        :return:
        """
        obj = instance.provider
        if not obj is None:
            return obj.description


class TypeLaunchAdmin(FinanceAdmin):
    inlines = [TypeActivityInline, ]
    search_fields = ('id', 'type_name', 'cost_fixo')
    list_display = ('id', 'cost_fixo', 'type_name', 'value_fixed', 'investment', 'sync')
    list_display_links = ('id', 'type_name', 'cost_fixo')
    ordering = ('-cost_fixo',)


class ContatoAdmin(FinanceAdmin):
    list_display = ('id', 'nome', 'telefone', 'data')


class PrevisionAdmin(FinanceAdmin):
    search_fields = ('id', 'provider__type_launch__type_name', 'description')
    list_display = ('id', 'description', 'date_expiration', 'paid', 'debit_prevision', 'credit_prevision', 'type_name', 'date_payment', 'sync')
    list_display_links = ('id', 'description', 'type_name', 'date_expiration', 'description')
    raw_id_fields = ('provider', )
    ordering = ('-date_expiration',)
    list_filter = ('provider__type_launch__type_name',)

    def type_name(self, instance):
        """
        :param instance: provider
        :return:
        """
        obj = instance.provider
        if not obj is None:
            return obj.type_launch.type_name


class ProviderAdmin(FinanceAdmin):
    search_fields = ('id', 'type_launch__type_name', 'date_last_purchase', 'description', )
    list_display = ('id', 'description', 'date_last_purchase', 'type_name', 'total_debit_week', 'total_credit_week', 'sync')
    list_display_links = ('id', 'type_name', 'date_last_purchase', 'description')
    # raw_id_fields = ('type_launch', )
    ordering = ('-date_last_purchase',)
    list_filter = ('type_launch__type_name',)

    def type_name(self, instance):
        """
        :param instance: type_launch
        :return:
        """
        obj = instance.type_launch
        if not obj is None:
            return obj.type_name


# from localflavor.br.forms import BRPhoneNumberField
# class MyModelFormAdmin(forms.ModelForm):
#     fone = BRPhoneNumberField(required=False, label='Telefone')
#     celular = BRPhoneNumberField(required=False, label='Celular')
#     class Meta: model = MyModel


class WeekNumberAdmin(FinanceAdmin):
    search_fields = ('id', 'num_week')
    ordering = ('-date_init',)
    list_display = ('id', 'date_init', 'date_final', 'num_week', 'value_week', 'value_debit_week', 'close_week',
                    'value_transf', 'value_invest', 'operation_broker', 'available_broker', 'value_trade', 'percent_result', 'sync')
    list_display_links = ('id', 'date_init', 'date_final', 'num_week')
    actions = ['sync_mycap', 'sync_itau', 'graphic_week']
    readonly_fields = ('date_init', 'date_final', 'num_week', 'close_week', 'date_closed' )
    # form = MyModelFormAdmin
    date_hierarchy = 'date_closed'
    fieldsets = (
        ('Semana', {
            'fields': ('num_week', 'date_init', 'date_final', 'close_week', 'date_closed', 'docfile_itau', 'docfile_mycap')
        }),
        ('Resultado', {
            'fields': ( 'value_week', 'value_debit_week',
                        'value_transf', 'value_invest', 'operation_broker',
                        'available_broker', 'value_trade', 'percent_result')
        }),
    )

    def get_queryset(self, request):
        qs = super(WeekNumberAdmin, self).get_queryset(request)
        return qs.order_by('-date_init')

    def sync_mycap(self, request, json_ext=None, queryset=None):
        """
        :param request:
        :param json_ext:
        :param queryset:
        :return:
        """
        try:
            sync_mycap.delay()
            self.message_user(request, "Requested synchronization with broker successfully executed.", level=messages.SUCCESS) #['ERROR', 'SUCCESS']
        except:
            self.message_user(request, "Operation not performed verify that RabbitMQ is running.", level=messages.ERROR)
    sync_mycap.short_description = "Synchronize broker"

    def sync_itau(self, request, json_ext=None, queryset=None):
        """
        :param request:
        :param json_ext:
        :param queryset:
        :return:
        """
        try:
            sync_itau.delay()
            self.message_user(request, "Requested synchronization with banc itau successfully executed.", level=messages.SUCCESS) #['ERROR', 'SUCCESS']
        except:
            self.message_user(request, "Operation not performed verify that RabbitMQ is running.", level=messages.ERROR)
    sync_itau.short_description = "Synchronize itau"

    def graphic_week(self, request, json_ext=None, queryset=None):
        """
        :param request:
        :param json_ext:
        :param queryset:
        :return:
        """
        try:
            sync_report.delay()
            self.message_user(request, "Requested graphic week with successfully executed.", level=messages.SUCCESS) #['ERROR', 'SUCCESS']
        except:
            self.message_user(request, "Operation not performed verify that RabbitMQ is running.", level=messages.ERROR)
    graphic_week.short_description = "Graphic week"


admin.site.register(Extract, ExtractAdmin)
admin.site.register(TypeLaunch, TypeLaunchAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Prevision, PrevisionAdmin)
admin.site.register(WeekNumber, WeekNumberAdmin)
admin.site.register(Contato, ContatoAdmin)
