# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime

from finance.models import * #WeekNumber #Document
from finance.forms import DocumentForm
import build.xlrd
# from utils.util import *
from utils.sync_report import *
from finance.extract import Extract
from finance.admin import WeekNumberAdmin

import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from .forms import WeeknumberForm
from rest_framework import generics, viewsets
from finance.serializers import *
from finance.week_number import WeekNumber
from django.contrib.auth.models import User, Group
from finance.contato import Contato

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ContatoList(generics.ListCreateAPIView):
	queryset = Contato.objects.all()
	serializer_class = ContatoSerializer


class ContatoDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Contato.objects.all()
	serializer_class = ContatoSerializer


class WeekNumberList(generics.ListCreateAPIView):
	queryset = WeekNumber.objects.all()
	serializer_class = WeekNumberSerializer


class WeekNumberDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = WeekNumber.objects.all()
	serializer_class = WeekNumberSerializer


def list(request):
		# Handle file upload
		if request.method == 'POST':
				form = DocumentForm(request.POST, request.FILES)
				if form.is_valid():
						docfile = request.FILES['docfile']
						if str(docfile)[-3:] == 'xls' and extract_mycap(docfile):
							invest = Investment()
							invest.import_extract_mycap(docfile)

						if str(docfile)[-3:] == "txt":
							newdoc = WeekNumber()
							wn = newdoc.get_or_create(None, docfile)

						ext = Extract()
						ext.importer_extract()
						num_week = datetime.today().isocalendar()[1]
						num_week_before = num_week - 1

						report_week( num_week_before )
						report_week( num_week )
						report_month( num_week )
						#return HttpResponseRedirect(reverse('finance.views.list'))
						return HttpResponseRedirect('admin/')
		else:
				form = DocumentForm() # A empty, unbound form

		# Load documents for the list page
		documents = WeekNumber.objects.exclude(docfile__isnull=True).exclude(docfile__exact="")
		# Render list page with the documents and the form
		return render_to_response(
				'finance/list.html',
				{'documents': documents, 'form': form},
				context_instance=RequestContext(request)
		)


class HomeView(TemplateView):
    template_name = 'weeknumber/home.html'


class AjaxTemplateMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'ajax_template_name'):
            split = self.template_name.split('.html')
            split[-1] = '_inner'
            split.append('.html')
            self.ajax_template_name = ''.join(split)
        if request.is_ajax():
            self.template_name = self.ajax_template_name
        return super(AjaxTemplateMixin, self).dispatch(request, *args, **kwargs)


class WeeknumberFormView(SuccessMessageMixin, AjaxTemplateMixin, FormView):
    template_name = 'weeknumber/test_form.html'
    form_class = WeeknumberForm
    success_url = reverse_lazy('home')
    success_message = "Way to go!"


# Create your views here.
def home(request):
    context = {}
    template = loader.get_template('home.html')
    data = RequestContext(request, context)
    return HttpResponse(template.render(data))

def admin(request):
    pass

# to get server time
def ajax_provider(request):
    # ext = Extract()
    # json_provider = ext.importer_extract()
    # json_provider = str(json_provider)
    _wn = WeekNumberAdmin(WeekNumber, WeekNumberAdmin)
    _wn.generate_report(request)
    json_provider = '[]'

    return HttpResponse(json_provider)
