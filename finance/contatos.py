# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.contrib.contenttypes.models import *
from .exceptions import IncorrectCellLabel
from utils.util import *
from django.db.models import Sum, Max
from django.contrib import messages
from django.db import transaction
from django.conf import settings
import os
from finance.type_launch import TypeLaunch


OPERADORAS = [
	{nome: "Oi", codigo: 14, categoria: "Celular", preco: 2},
	{nome: "Vivo", codigo: 15, categoria: "Celular", preco: 1},
	{nome: "Tim", codigo: 41, categoria: "Celular", preco: 3},
	{nome: "GVT", codigo: 25, categoria: "Fixo", preco: 1},
	{nome: "Embratel", codigo: 21, categoria: "Fixo", preco: 2}
]

class Contato(models.Model):
    # id = models.IntegerField(primary_key=True)  # AutoField?
    nome = models.CharField(max_length=50, unique=True)
    telefone = models.CharField(max_length=10, unique=True)
    data = models.DateField('date contato')
    operadoras = models.CharField(max_length=10, choices=OPERADORAS)

    def __unicode__(self):
        return self.nome

    def __str__(self):
        return self.nome

    # class Meta:
    #     managed = True
    #     db_table = 'finance_contato'
