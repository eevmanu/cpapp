# coding=utf-8

import re

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

# from validate_email import validate_email


class UniqueEmailField(forms.EmailField):

    def __init__(self, *args, **kwargs):
        super(UniqueEmailField, self).__init__(
            max_length=75,
            *args, **kwargs
        )

    def clean(self, value):
        super(UniqueEmailField, self).clean(value)

        # if not validate_email(value):
        #     raise forms.ValidationError(_(u"Email inválido"))

        value = value.lower()
        if User.objects.filter(email=value).count() > 0:
            raise forms.ValidationError(_(u"Email ya registrado"))
        return value

name_regex = re.compile(r'^[ \'a-zA-Z]+?$', re.U)


class NameField(forms.CharField):

    def __init__(self, *args, **kwargs):
        super(NameField, self).__init__(
            # min_length=5,
            max_length=100,
            *args, **kwargs
        )

    def clean(self, value):
        super(NameField, self).clean(value)
        if not self.required:
            return value if value else u''
        if not name_regex.match(value):
            raise forms.ValidationError(_(u"Nombres y/o apellidos invalidos"))
        return value

password_regex = re.compile(r'^[\w\+]+?$', re.U)


class PasswordField(forms.CharField):

    def __init__(self, *args, **kwargs):
        super(PasswordField, self).__init__(
            min_length=5,
            # max_length=20,
            *args, **kwargs
        )

    def clean(self, value):
        super(PasswordField, self).clean(value)

        if not password_regex.match(value):
            raise forms.ValidationError(_(u"La contraseña solo debe incluir letras y/o números."))

        # Passwordmeter for check strength password
        # if check_strength(password) is not enough:
        #     raise forms.ValidationError(_(u""))

        return value


class SignupForm(forms.Form):
    email = UniqueEmailField()
    password = PasswordField()
    reg_id = forms.CharField()
    first_name = NameField()
    last_name = NameField()


class SigninForm(forms.Form):
    email = forms.EmailField()
    password = PasswordField()
    reg_id = forms.CharField()

    def clean_email(self):
        return self.cleaned_data['email'].lower()


class SigninFBForm(forms.Form):
    email = forms.EmailField()
    fb_id = forms.IntegerField()
    reg_id = forms.CharField()
    token = forms.CharField()
    first_name = NameField(required=False)
    last_name = NameField(required=False)

    def clean_email(self):
        return self.cleaned_data['email'].lower()
