from django.conf import settings
from django.utils.translation import activate
from datetime import datetime

def log_write(request):
    user_agent = request.META.get('HTTP_USER_AGENT')
    if user_agent is not None and 'YandexMetrika' in user_agent:
        return None
    log_row = {
        'ip': request.META.get('REMOTE_ADDR', '127.0.0.1'),
        'port': int(request.META.get('REMOTE_PORT', '0')),
        'method': request.META.get('REQUEST_METHOD', 'GET'),
        'path': request.path,
        'query_get': request.GET.__str__(),
        'query_post': request.POST.__str__(),
        'sessionid': request.COOKIES.get('sessionid', ''),
        'http_referer': request.META.get('HTTP_REFERER', ''),
        'http_user_agent': user_agent,
    }
    if request.user.is_authenticated():
        log_row['user'] = request.user
    import os
    os.system('echo "[{}] - {}" >> /tmp/log_tram'.format(datetime.now().ctime(), str(log_row).replace('"', '\"')))

class LanguageMiddleware(object):
    def process_view(self, request, view, args, kwargs):
#        try:
#            log_write(request)
#        except:
#            pass
        user = request.user
        is_auth = user.is_authenticated()
        user_lang = is_auth and user.language or settings.LANGUAGE_CODE
	def_lang = request.session.get('language', user_lang)
        lang = kwargs.get('lang', def_lang) or def_lang

        request.LANGUAGE_CODE = lang
        activate(lang)
