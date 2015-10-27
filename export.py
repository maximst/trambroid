#!/usr/bin/env python
#-*- coding: utf-8 -*-
import django
django.setup()

import psycopg2
import random
import re
import sys
from datetime import datetime
from django.contrib.auth import get_user_model
from unidecode import unidecode
from apps.content.models import Blog, Comment
from apps.drupal.functions import text_summary
from django.template.defaultfilters import slugify, removetags

host='localhost'
user = sys.argv[1]
passwd = sys.argv[2]
dbase = sys.argv[3]

User = get_user_model()


db = psycopg2.connect(host=host, user=user, password=passwd, dbname=dbase)
cursor = db.cursor()

#cursor.execute('SET NAMES "utf8"')


#BEGIN export users
all_users = User.objects.all()
all_users.delete()

cursor.execute('''SELECT
        users.uid,
        users.name,
        users.mail,
        users.signature,
        users.created,
        users.status,
        users.timezone,
        users.language,
        users.pass,
        file_managed.uri,
        users.created,
        users.login,
        url_alias.alias
    FROM users
    LEFT OUTER JOIN file_managed ON users.picture = file_managed.fid
    LEFT OUTER JOIN url_alias ON 'blog/' || users.uid = url_alias.source
    WHERE users.status > 0 AND users.uid > 0
    ORDER BY users.uid''')
users = cursor.fetchall()

for row in users:
    lname = ''
    fullname = row[1].split(' ')

    if len(fullname) == 1:
        fullname = row[1].split('_')

    fname = fullname[0]

    if len(fullname) >= 2:
        lname = fullname[1]

    if row[6] is None:
        tz = 'Europe/Kiev'
    else:
        tz = row[6]

    avatar = row[9]
    if avatar is not None:
        avatar = avatar.replace('public://', '').replace('sites/default/files/', '').replace('pictures/', 'avatars/')

    print row

    us = User.objects.get_or_create(
        username=unicode(row[1], 'utf8')[:30],
        defaults={
            'avatar': avatar,
            'timezone': unicode(tz, 'utf8'),
            'signature': unicode(row[3], 'utf8'),
            'language': unicode(row[7] or 'ru', 'utf8'),
            'first_name': unicode(fname, 'utf8')[:30],
            'last_name': unicode(lname, 'utf8')[:30],
            'email': unicode(row[2], 'utf8')[:75],
            'drupal_uid': row[0],
            'drupal_password': row[8],
            'is_staff': (row[0] == 1),
            'is_superuser': (row[0] == 1),
            'is_active': True,
            'date_joined': datetime.fromtimestamp(row[10]),
            'last_login': datetime.fromtimestamp(row[11]),
            'drupal_blogs_alias_url': row[12]
        }
    )
#END export users



#BEGIN export content
all_content = Blog.objects.all()
all_content.delete()

query = '''SELECT
  node.nid,
  node.language,
  node.title,
  node.uid,
  node.created,
  node.changed,
  field_data_body.body_value,
  field_data_body.body_summary,
  node.type,
  promote,
  node.sticky,
  field_data_body.body_format,
  node.status
 FROM node
 LEFT JOIN field_data_body
 ON node.nid = field_data_body.entity_id
 ORDER BY node.nid'''

cursor.execute(query)

result = cursor.fetchall()

def save(result):
    for row in result:
        if row[1] not in ('ru', 'en'):
            lang = 'ru'
        else:
            lang = row[1]

        cursor.execute("SELECT alias FROM url_alias WHERE source = 'node/%i'" % row[0])
        try:
            drupal_slug = cursor.fetchall()[0][0]
        except:
            drupal_slug = ''

        slug = slugify(unidecode(unicode(row[2], 'utf8')))
        if Blog.objects.filter(slug=slug).exists():
            slug += '-{}'.format(hex(random.randint(0, 65535))[2:].rjust(4, '0'))

        try:
            usr = User.objects.get(drupal_uid=row[3])
        except User.DoesNotExist:
            usr = None

        title = row[2]

        if row[6] is None:
            body = ''
        else:
            body = unicode(row[6], 'utf8')
            if row[11] not in ('full_html', 'filtered_html', 'video_filter', 'php_code'):
                body = body.replace('\n', '\n<br />\n')

        if row[7]:
            preview = unicode(row[7], 'utf8')
        else:
            preview = text_summary(body, row[11], 600)

        print row[8], title

        bl = Blog.objects.language(lang).get_or_create(
            drupal_nid=row[0],
            defaults={
                'name': u'drupal/node/{} - {}'.format(row[0], unicode(title, 'utf8')),
                'title': unicode(title, 'utf8'),
                'user': usr,
                'create_time': datetime.fromtimestamp(row[4]),
                'edit_time': datetime.fromtimestamp(row[5]),
                'body': body,
                'preview': preview,
                'slug': slug,
                'drupal_slug': unicode(drupal_slug, 'utf8'),
                'drupal_type': unicode(row[8], 'utf8'),
                'front_page': bool(row[9]),
                'on_top': bool(row[10]),
                'is_active': bool(row[12])
            }
        )

save(result)


#END export content

#BEGIN export comments
Comment.objects.all().delete()

query = '''SELECT
  comment.nid,
  comment.pid,
  comment.uid,
  comment.subject,
  comment.created,
  comment.changed,
  comment.hostname,
  field_data_comment_body.comment_body_value,
  field_data_comment_body.comment_body_format,
  comment.cid,
  comment.language
 FROM comment
 LEFT JOIN field_data_comment_body
 ON comment.cid = field_data_comment_body.entity_id
 WHERE comment.status > 0
 ORDER BY comment.cid'''

cursor.execute(query)

cid_map = {}
for row in cursor.fetchall():
    try:
        blog = Blog.objects.get(drupal_nid=row[0])
    except Blog.DoesNotExist:
        continue

    try:
        usr = User.objects.get(drupal_uid=row[2])
    except User.DoesNotExist:
        usr = None

    if row[8] in ('plain_text', 'anonimous_comment'):
        body = removetags(row[7], 'a')
    else:
        body = unicode(row[7], 'utf8')

    if row[10] == 'und':
        lang = u'ru'
    else:
        lang = unicode(row[10], 'utf8')

    r = re.compile((r'(?P<quote><\s*div[^>]+class\s*=\s*(?:"|\')?\s*quote\s*(?:"|\')?[^>]*>'
        r'(?P<quote_body_all>[^<]*(?:<\s*div[^>]+class\s*=\s*(?:"|\')?\s*quotp-author\s*(?:"|\')?[^>]*>)?'
        r'[^<]*(?:<\s*b\s*>)?(?P<author>[^<]+)?(?:<\s*\/\s*b\s*>)?[^<]*'
        r'(?:<\s*\/\s*div\s*>)?'
        r'[^<]*(?:<\s*div[^>]+class\s*=\s*(?:"|\')?\s*quote-msg\s*(?:"|\')?[^>]*>)?'
        r'(?P<quote_body>[^<]*)'
        r'(?:<\s*\/\s*div\s*>)?)'
        r'<\s*\/\s*div\s*>)+'), re.I)

    for i in r.finditer(body):
        res = i.groupdict()
        quote = res.get('quote')
        quote_body = res.get('quote_body')
        quote_body_all = res.get('quote_body_all')
        author = res.get('author')

        if quote:
            if author:
                new_quote = u'[quote author="{}"]'.format(author)
            else:
                new_quote = u'[quote]'

            if quote_body:
                new_quote += quote_body
            else:
                new_quote += quote_body_all

            new_quote += u'[/quote]'

            body = body.replace(quote, new_quote)

    comment = Comment.objects.create(
        title=unicode(row[3], 'utf8'),
        body=body,
        user=usr,
        create_time=datetime.fromtimestamp(row[4]),
        edit_time=datetime.fromtimestamp(row[5]),
        ip=row[6],
        blog=blog,
        language=lang or u'ru'
    )
    print 'Comment ', comment.id, ' is created'
    cid_map[row[9]] = comment.id

query = '''SELECT
  comment.cid,
  comment.pid
 FROM comment
 WHERE comment.pid > 0 AND comment.status > 0
 ORDER BY comment.cid'''

cursor.execute(query)

for row in cursor.fetchall():
    comment = Comment.objects.get(id=cid_map[row[0]])
    parent = Comment.objects.get(id=cid_map[row[1]])
    print 'For comment ', comment.id, ' set parent ', parent.id
    comment.parent = parent
    comment.save()

#END export comments
