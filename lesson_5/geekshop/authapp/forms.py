import hashlib

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from authapp.models import ShopUser, ShopUserProfile

import pytz
from datetime import datetime
from django.conf import settings


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'email', 'age', 'avatar', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def clean_age(self):
        data = self.cleaned_data['age']
        if data > 100:
            raise forms.ValidationError('Со всем почтением Ваш возраст слишком велик.')
        return data

    def clean_username(self):
        data = self.cleaned_data['username']
        if len(data) > 24:
            raise forms.ValidationError('Слишком длинный ник.')
        return data

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if len(data) > 24:
            raise forms.ValidationError('Слишком длинное имя.')
        return data

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.is_active = False

        # Вариант для боевого использования
        # import random, hashlib
        # salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        # user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()

        user.activate_key = hashlib.sha1(user.email.encode('utf8')).hexdigest()
        user.activate_key_expired = datetime.now(pytz.timezone(settings.TIME_ZONE))
        user.save()
        return user


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'email', 'age', 'avatar', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()

    def clean_age(self):
        data = self.cleaned_data['age']
        if data > 100:
            raise forms.ValidationError('Со всем почтением Ваш возраст слишком велик.')
        return data

    def clean_username(self):
        data = self.cleaned_data['username']
        if len(data) > 24:
            raise forms.ValidationError('Слишком длинный ник.')
        return data

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if len(data) > 24:
            raise forms.ValidationError('Слишком длинное имя.')
        return data


class ShopUserProfileEditForm(forms.ModelForm):

    class Meta:
        model = ShopUserProfile
        exclude = ('user',)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'
                field.help_text = ''