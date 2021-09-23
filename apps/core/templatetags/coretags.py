#-*- coding: utf-8 -*-
from django import template
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Page
from django.utils import html
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.template.defaultfilters import stringfilter

from voting.models import Vote
from apps.content.models import Blog

import re
import zlib
import urllib
import sqlite3

register = template.Library()

@register.filter
def diff(value, arg):
    return int(value) - arg

@register.inclusion_tag('menubar.html', takes_context=True)
def menubar(context):
    request = context.get('request')
    sections = []
    for name, title in settings.MENU_ITEMS:
        try:
            url = reverse(name)
        except:
            url = '#'
        sections.append({'name': name, 'title': title, 'url': url})
    lang = request and request.LANGUAGE_CODE or 'ru'
    for blog in Blog.objects.language(lang).filter(in_menu=True, is_active=True):
        sections.append({'name': blog.name, 'title': blog.title,
                         'url': blog.get_absolute_url()})

    sections_rev = list(sections)
    sections_rev.reverse()
    current = None
    for sr in sections_rev:
        if request and sr['url'] in request.META['PATH_INFO']:
            current = sr
            break

    context.update({'current_section': current, 'sections': sections})
    return context

@register.inclusion_tag('breadcrump.html', takes_context=True)
def breadcrump(context):
    request = context.get('request')
    if request:
        crumps = request.META['PATH_INFO'].split('/')[:-1]
    else:
        crumps = ['/']

    urls = list(map(lambda c: crumps[:crumps.index(c)+1], crumps))
    urls[0].append(u'')

    titles = ['home'] + crumps[1:]

    crumps = zip(urls, titles)
    return {'crumps': crumps}

@register.inclusion_tag('vote.html', takes_context=True)
def vote(context):
    if not isinstance(context['content'], Page):
        ct = ContentType.objects.get_for_model(context['content'].__class__)
    score = Vote.objects.get_score(context['content'])
    return {'app': ct.app_label, 'model': ct.model, 'pk': context['content'].pk,
                              'score': score, 'user': context['request'].user}


@register.filter
def quoted_text(text):
    r = re.compile(settings.QUOTE_REGEX, re.I+re.S)
    r_arg = re.compile(r'([a-z0-9]+)\s*=\s*"?((?:(?!(?:"?\s*[a-z0-9]+\s*=|")).)+)"?', re.I+re.S)
    result = r.finditer(text)

    text = text.replace('\n', '<br />')
    for r in result:
        res = r.groupdict()
        author = res.get('author')
        res['quote_body'] = res['quote_body'].strip().replace('\n', '<br />')
        quote = res.get('quote', '').replace('\n', '<br />')

        if not author:
            args = r_arg.finditer(res.get('args', ''))
            args = dict(r.groups() for r in args)
            res.update(args)

        if quote:
            new_quote = render_to_string('quote.html', res)
            text = text.replace(quote, new_quote)

    return text


@register.filter
def format_text(text, data=None):
    try:
        return text % data
    except:
        return text


@register.filter
@stringfilter
def rupluralize(value, arg):
    bits = arg.split(u',')
    try:
        if str(value).endswith('1'):
            return bits[0]
        elif str(value)[-1:] in '234':
            return bits[1]
        else:
            return bits[2]
    except:
        raise template.TemplateSyntaxError
    return ''
rupluralize.is_safe = False


@register.simple_tag(takes_context=True)
def links(context):
    request = context.get('request')
    if request:
        url = request.META.get('PATH_INFO', '')
        url_list = url.split('://')
        if len(url_list) > 1:
            url = '://'.join(url_list[1:])

        if url.startswith('/'):
            url = u'trambroid.com%s' % url

        query_string = request.META.get('QUERY_STRING')
        if query_string:
            url += '?%s' % query_string
    else:
        url = u'trambroid.com/'

    if url.endswith('/'):
        alt_url = url[:-1]
    else: 
        alt_url = '{}/'.format(url)

    quoted_url = urllib.parse.quote(url.encode('utf-8'))
    alt_quoted_url = urllib.parse.quote(alt_url.encode('utf-8'))

#    print quoted_url

    conn = sqlite3.connect(settings.LINKS_DB)
    sql = conn.cursor()

    links = []
    for provider in ['mainlink', 'linkfeed']:
        try:
            res = sql.execute('SELECT * FROM {} WHERE url = ? OR url = ? OR url = ? OR url = ?'.format(provider), (url, alt_url, quoted_url, alt_quoted_url))

            for link in res:
                links.append(u'<li>%s</li>' % link[2])
        except Exception:
            pass

    return html.format_html('<ul class="linx unstyled cached">{}</ul>', html.mark_safe('\n'.join(links)))


@register.simple_tag(takes_context=True)
def setlinks(context):
    request = context.get('request')
    if not request:
        return ''

    full_url = request.build_absolute_uri()
    crc_uri_1 = str(zlib.crc32(full_url[12:].encode()) % (1<<32))
    crc_uri_2 = str(zlib.crc32(full_url.encode()) % (1<<32))

    qs = urllib.parse.urlencode({
        'host': 'trambroid.com',
        'p': '6d6e10342d591fd102032427afb42eca',
    })
    setlinks_url = 'http://show.setlinks.ru/?%s' % qs

    def _filter(row):
        row_list = row.split()
        return row_list and row_list[0] in (crc_uri_1, crc_uri_2) or False

    try:
        result = urllib.request.urlopen(setlinks_url, timeout=3)
        result = result.code == 200 and result.readlines() or None
    except:
        return ''
    else:
        res = result and list(filter(_filter, result)) or None
        return res and res[0].decode('cp1251').replace(res[0].split()[0], '<!--6d6e1-->') or ''

    if request:
        url = request.META.get('PATH_INFO', '')
        url = url.endswith('/') and url[:-1] or url
        query_string = request.META.get('QUERY_STRING')
        if query_string:
            url += '?%s' % query_string
    else:
        url = '/'

    setlinks_querystring = urllib.parse.urlencode({
        'host': 'trambroid.com',
        'start': '1',
        'count': '20',
        'p': '6d6e10342d591fd102032427afb42eca',
        'uri': url.encode('utf-8'),
    })
    setlinks_url = 'http://show.setlinks.ru/page.php?%s' % setlinks_querystring

    try:
        result = urllib.request.urlopen(setlinks_url, timeout=5)
    except:
        return ''
    else:
        if result.code == 200:
            return result.read()

    return ''


@register.filter
@stringfilter
def replace(value, arg):
    from_str, to_str = arg.split("'/'")
    from_str = from_str[1:]
    to_str = to_str[:-1]
    return value.replace(from_str, to_str)
replace.is_safe = False
