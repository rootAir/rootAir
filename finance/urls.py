# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.views.generic.base import RedirectView
# from .views import HomeView, WeeknumberFormView
from .admin import WeekNumberAdmin

urlpatterns = patterns('finance.views',
    # url(r'^$', 'list', name='list'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', HomeView.as_view(), name="home"),
    # url(r'^weeknumber-form/$', WeeknumberFormView.as_view(), name="weeknumber-form"),
    url(r'^ajax_provider/?$', 'ajax_provider', name='ajax_provider'),
    url(r'^$', RedirectView.as_view(url='/admin/finance/weeknumber/'), name='weeknumber'),
);

# urlpatterns = patterns('finance.admin',
#     url(r'^teste/?$', WeekNumberAdmin.teste(), name='teste'),
# );