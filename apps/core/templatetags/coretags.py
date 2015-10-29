#-*- coding: utf-8 -*-
from django import template
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.paginator import Page
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from django.template.defaultfilters import stringfilter

from voting.models import Vote
from apps.content.models import Blog

import re
import urllib
import urllib2

register = template.Library()

@register.filter
def diff(value, arg):
    return int(value) - arg

@register.inclusion_tag('menubar.html', takes_context=True)
def menubar(context):
    request = context['request']
    sections = []
    for name, title in settings.MENU_ITEMS:
        try:
            url = reverse(name)
        except:
            url = '#'
        sections.append({'name': name, 'title': title, 'url': url})
    lang = request.LANGUAGE_CODE
    for blog in Blog.objects.language(lang).filter(in_menu=True, is_active=True):
        sections.append({'name': blog.name, 'title': blog.title,
                         'url': blog.get_absolute_url()})

    sections_rev = list(sections)
    sections_rev.reverse()
    current = None
    for sr in sections_rev:
        if sr['url'] in request.META['PATH_INFO']:
            current = sr
            break

    context.update({'current_section': current, 'sections': sections})
    return context

@register.inclusion_tag('breadcrump.html', takes_context=True)
def breadcrump(context):
    crumps = context['request'].META['PATH_INFO'].split('/')[:-1]

    urls = map(lambda c: crumps[:crumps.index(c)+1], crumps)
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
def setlinks(context):
    request = context['request']
    url = request.META.get('PATH_INFO', '')
    query_string = request.META.get('QUERY_STRING')
    if query_string:
        url += '?%s' % query_string


    setlinks_querystring = urllib.urlencode({
        'host': 'trambroid.com',
        'start': '1',
        'count': '20',
        'p': '6d6e10342d591fd102032427afb42eca',
        'uri': url,
    })
    setlinks_url = 'http://show.setlinks.ru/page.php?%s' % setlinks_querystring

    try:
        result = urllib2.urlopen(setlinks_url, timeout=5)
    except:
        return None
    else:
        if result.code == 200:
            return result.read()
    return None