from django.contrib import admin
from .activity import Activity
from .type_activity import TypeActivity
from finance.type_launch import TypeLaunch
from .planned import Planned
from utils.util import *
from django.http import HttpResponsePermanentRedirect
from nvd3 import cumulativeLineChart
from nvd3 import linePlusBarChart
from nvd3 import pieChart
from finance.week_number import *
import random
import datetime
import time

class ActivityAdmin(admin.ModelAdmin):

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


class TypeLaunchInline(admin.TabularInline):
    model = TypeLaunch
    extra = 1
    raw_id_fields = ('id', 'type_name',)


class PlannedAdmin(ActivityAdmin):
    search_fields = ('description', 'date_activity')
    list_display = ('id', 'description', 'date_activity', 'type_activity', 'hour_init', 'hour_final', 'time_total',
                    'checked', 'state', 'check_list', 'synchronized')
    list_display_links = ('description', 'date_activity', 'type_activity')
    list_filter = ('type_activity__type_desc',)
    ordering = ('-date_activity', 'type_activity')


# class TypeActivityAdmin(ActivityAdmin):
#     # inlines = [TypeLaunchInline,]
#     search_fields = ('type_name', 'type_desc', 'type_launch__type_name')
#     list_display = ('id', 'type_name', 'type_desc', 'cost_fixed', 'value_fixed', 'group', 'positive', 'sync')
#     list_display_links = ('id', 'type_name','cost_fixed', 'type_desc')
#     list_filter = ('type_launch__type_name',)
#     # raw_id_fields = ('type_launch',)
#     ordering = ('-positive',)
#     # fields = ['type_launch',]
#     # fieldsets = [
#     #     ('Type Launch', {'fields': ['type_name',], 'classes': ['TypeLaunch']}),
#     # ]
#
#     def cost_fixed(self, instance):
#         """
#         :param instance:
#         :return:
#         """
#         obj = instance.type_launch
#         if not obj is None:
#             return obj.type_name
#
#     def value_fixed(self, instance):
#         """
#         :param instance:
#         :return:
#         """
#         obj = instance.type_launch
#         if not obj is None:
#             return obj.value_fixed
#
#     def get_queryset(self, request):
#         """
#         :param request:
#         :return:
#         """
#         qs = super(self.__class__, self).get_queryset(request)
#         return qs.select_related()

#
# class ActivityAdmin(ActivityAdmin):
#     #inlines = [ProviderInline, ]
#     search_fields = ('description', 'date_activity')
#     list_display = ('id', 'description', 'date_activity', 'time_total', 'type_name', 'hour_init', 'hour_final', 'calendar', 'sync')
#     list_display_links = ('id', 'description', 'date_activity', 'time_total', 'type_name')
#     # raw_id_fields = ('type_activity',)
#     ordering = ('-date_activity', 'hour_init')
#     actions = ['graphic_activity']
#
#     def type_name(self, instance):
#         """
#         :param instance:
#         :return:
#         """
#         obj = instance.type_activity
#         if not obj is None:
#             return obj.type_desc


# admin.site.register(TypeActivity, TypeActivityAdmin)
# admin.site.register(Activity, ActivityAdmin)
admin.site.register(Planned, PlannedAdmin)

