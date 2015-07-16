# -*- coding: utf-8 -*-
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

# class UploadFileForm(forms.Form):
#     title = forms.CharField(max_length=50)
#     file = forms.FileField()

class WeeknumberForm(forms.Form):
    # date_launch = forms.CharField(required=True)
    # launch = forms.CharField(required=True)
    # date_purchase = forms.CharField(required=True)
    # value_debit = forms.CharField(required=True)
    # value_credit = forms.CharField(required=True)
    # value_balance = forms.CharField(required=True)
    # cancelled = forms.CharField(required=True)
    # provider = forms.CharField(required=True)
    # comment = forms.CharField(required=True, widget=forms.Textarea)

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False # don't render form DOM element
        helper.render_unmentioned_fields = True # render all fields
        helper.label_class = 'col-md-2'
        helper.field_class = 'col-md-10'
        return helper


class ContactForm(forms.Form):

    name = forms.CharField(
        label = "Name:",
        max_length = 80,
        required = True,
    )

    email = forms.CharField(
        label = "E-mail:",
        max_length = 80,
        required = True,
    )

    subject = forms.CharField(
        label = "Subject:",
        max_length = 80,
        required = True,
    )

    message = forms.CharField(
        widget = forms.Textarea,
        label = "Message:",
        required = True,
    )

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('send', 'Send'))
