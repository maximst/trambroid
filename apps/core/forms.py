#-*- coding: utf-8 -*-
from io import StringIO
from django import forms
from django.conf import settings
from django.core.files import File
from django.contrib.auth import get_user_model
import supercaptcha
from pytz import all_timezones
from PIL import Image


User = get_user_model()


class RegistrationForm(forms.Form):
    username = forms.CharField(required=True, label='Имя пользователя')
    password = forms.CharField(required=True, label='Пароль', widget=forms.PasswordInput)
    first_name = forms.CharField(required=False, label='Имя')
    last_name = forms.CharField(required=False, label='Фамилия')
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False, label='Аватар')
    #sex = forms.IntegerField(label='Пол',
                      #widget=forms.Select(choices=User.SEX_CHOICES))
    #bdate = forms.DateField(required=False, label='Дата рождения')
    #location = forms.CharField(max_length=255, required=False, label='Откуда')
    timezone = forms.CharField(max_length=32, initial='Europe/Kiev',
                              label='Временная зона',
            widget=forms.Select(choices=zip(all_timezones, all_timezones)))
    signature = forms.CharField(max_length=255, widget=forms.Textarea,
                                        required=False, label='Подпись')
    captcha = supercaptcha.CaptchaField(label=u'Введите текст с картинки')


    def save(self, avatar=None):
        try:
            user = User.objects.get(username=self.cleaned_data['username'])
        except:
            user = None

        if user:
            user_errors = self.errors.get('username')
            if user_errors:
                self.errors['username'].append(
                    u'Такой пользователь уже существует.'
                )
            else:
                self.errors.update({'username':\
                forms.util.ErrorList([u'Такой пользователь уже существует.'])})
            raise forms.ValidationError(u'Такой пользователь уже существует.')

        user = User(username=self.cleaned_data['username'])
        user.save()
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.set_password(self.cleaned_data['password'])
        user.is_active = False
        user.save()

        #user.bdate = self.cleaned_data['bdate']
        #user.sex = self.cleaned_data['sex']
        #user.location = self.cleaned_data['location']
        user.timezone = self.cleaned_data['timezone']
        user.signature = self.cleaned_data['signature']

        if avatar:
            if avatar.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
                raise forms.ValidationError(u'Размер изображения превышает %i\
                  Мб.' % (settings.FILE_UPLOAD_MAX_MEMORY_SIZE / (1024*1024)))

            img_temp = StringIO(avatar.read())

            img = Image.open(img_temp)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            min_side = min(img.size)
            max_side = max(img.size)
            offsets = [0, 0]
            size = [min_side, min_side]
            offsets[img.size.index(max_side)] = (max_side - min_side) / 2
            size[img.size.index(max_side)] = min_side + max(offsets)
            img = img.crop((offsets[0], offsets[1], size[0], size[1]))
            img = img.resize(settings.AVATAR_SIZE, Image.ANTIALIAS)
            f = StringIO()
            img.save(f, 'PNG')

            img_filename = '%i.png' % user.pk

            if user.avatar.name != user.avatar.field.default:
                user.avatar.storage.delete(user.avatar.name)
            user.avatar.save(img_filename, File(f))

        user.save()
        return user.pk
