from django.contrib.auth.models import User
from django import forms
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.localflavor.us.forms import USPhoneNumberField

from lightning_app.models import *

class AccountForm(forms.Form):
	location = forms.CharField()
	website = forms.URLField()
	about = forms.CharField(widget=forms.Textarea)
	phone = USPhoneNumberField()
