from django.contrib.auth import login
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings

from urllib2 import urlopen
import vkontakte
from StringIO import StringIO
from PIL import Image
from datetime import date
from pyfaceb import FBGraph


def set_user_profile(backend, user, response, uid, *args, **kwargs):
    print backend.data
    if user and backend.name == 'facebook':
        facebook_api = 'http://graph.facebook.com/%s/picture?type=large' %\
                                                 str(uid)
        image_url = urlopen(facebook_api).url
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(image_url).read())

#        img = Image.open(img_temp)
#        if img.mode != 'RGB':
#            img = img.convert('RGB')
#        min_side = min(img.size)
#        max_side = max(img.size)
#        offsets = [0, 0]
#        size = [min_side, min_side]
#        offsets[img.size.index(max_side)] = (max_side - min_side) / 2
#        size[img.size.index(max_side)] = min_side + max(offsets)
#        img = img.crop((offsets[0], offsets[1], size[0], size[1]))
#        img = img.resize(settings.AVATAR_SIZE, Image.ANTIALIAS)
#        f = StringIO()
#        img.save(f, 'PNG')
#
        img_filename = '%i-%s.png' % (user.id, user.username)
        user.avatar.save(img_filename, img_temp)

        fb = FBGraph(response['access_token'])
        me = fb.get('me')
        user.locale = response.get('locale', me.get('locale', 'ru'))
        #TODO: save timezone

        #user.sex = GENDER.get(me['gender'], 0)
        #bdate = me['birthday'].split('/')
        #bdate = map(int, bdate)
        #user.bdate = date(bdate[2], bdate[0], bdate[1])
        user.save()

    if user and backend.name == 'vk-oauth2':
        vk_api = vkontakte.API(token=response['access_token'])
        result = vk_api.users.get(fields='sex,bdate,photo_200,personal,country,city,timezone,status',
                                                                     uids=uid)
        image_url = result[0]['photo_200']
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(image_url).read())

        img_filename = '%i-%s.png' % (user.id, user.username)
        user.avatar.save(img_filename, img_temp)

        user.locale = result[0].get('personal', {'langs': 'ru'}).get('langs', 'ru')
        #user.timezone = result[0].get('timezone', 'Europe/Kiev')
        user.signature = result[0].get('status', '')

        user.save()

#        img_temp = StringIO(urlopen(image_url).read())
#        img_temp.flush()
#
#        img = Image.open(img_temp)
#        if img.mode != 'RGB':
#            img = img.convert('RGB')
#        f = StringIO()
#        img.save(f, 'PNG')
#
#        img_filename = '%i.png' % usa.user_id
#        uprof.avatar.save(img_filename, File(f))
#        uprof.sex = result[0]['sex']
#        bdate = result[0]['bdate'].split('.')
#        bdate.reverse()
#        if len(bdate) == 2:
#            bdate.insert(0, '0')
#        uprof.bdate = date(*map(int, bdate))
#        uprof.save()
