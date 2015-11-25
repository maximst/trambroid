#-*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.core.files import File
from django.contrib.auth import get_user_model, forms as auth_forms
from django.utils.translation import ugettext_lazy as _

from registration.forms import RegistrationFormUniqueEmail

import supercaptcha
from pytz import all_timezones
from PIL import Image
from StringIO import StringIO


User = get_user_model()


class ProfileFormMixin(object):
    first_name = forms.CharField(required=False, label=_(u'Имя'))
    last_name = forms.CharField(required=False, label=_(u'Фамилия'))
    language = forms.CharField(max_length=5, initial='ru', label=_(u'Язык'),
                required=False, widget=forms.Select(choices=settings.LANGUAGES))
    timezone = forms.CharField(max_length=32, initial='Europe/Kiev',
                label=_(u'Временная зона'), required=False,
                widget=forms.Select(choices=zip(all_timezones, all_timezones)))
    avatar = forms.ImageField(required=False, label=_(u'Аватар'))
    signature = forms.CharField(max_length=255, initial='', required=False,
        widget=forms.Textarea(attrs={'class': 'signature-form'}), label=_(u'Подпись'))
    stupidity_level = forms.IntegerField(required=False, label=_(u'Уровень глупости'), 
                        widget=forms.Select(choices=settings.STUPIDITY_LEVELS))


class RegistrationForm(ProfileFormMixin, RegistrationFormUniqueEmail):
#    captcha = supercaptcha.CaptchaField(label=_(u'Введите текст с картинки'))

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "language",
            "timezone",
            "avatar",
            "signature",
            "stupidity_level",
        )


class ProfileForm(ProfileFormMixin, auth_forms.UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for k in self.fields:
            self.fields[k].required = False
        self.fields['avatar'].widget.clear_checkbox_label = _('Delete')
        self.fields['avatar'].widget.template_with_initial = (
            '<br />%(input)s<br /><br />%(clear_template)s'
        )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "language",
            "timezone",
            "avatar",
            "signature",
            "stupidity_level",
        )

    def clean_password(self):
        return self.initial.get("password", self.instance.password)
