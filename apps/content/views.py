# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.db.models import Count, Q

from models import Blog, Comment
from forms import CommentForm
#from apps.core.decorators import ajax_navigation

from taggit.models import Tag
import os


def blog_detail(request, slug, lang='ru', is_drupal=False, path=None):
    user = request.user
    lang = request.LANGUAGE_CODE

    qs = Blog.objects.language('all')
    query = Q(is_active=True)
    if is_drupal and slug.isdigit() and path:
        drupal_slug = os.path.join(path, slug)
        query &= (Q(drupal_nid=int(slug)) | (~Q(drupal_nid=int(slug)) & Q(drupal_slug=drupal_slug)))
    elif is_drupal and slug.isdigit():
        query &= Q(drupal_nid=int(slug))
    elif is_drupal:
        query &= Q(drupal_slug=slug)
    else:
        query &= Q(slug=slug)
        qs = Blog.objects.language(lang)

    try:
        content = get_object_or_404(qs, query)
    except Http404:
        if slug.isdigit():
            content = get_object_or_404(qs, is_active=True, id=slug)
        else:
            raise Http404

    context = {'content': content, 'page_title': ' | %s' % content.title}
    context.update(csrf(request))

    if request.method == 'POST' and user.is_authenticated():
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            ip = request.META.get('REMOTE_ADDR')
            language = user.language
            comment_form.save(content, user, ip, language)
            return redirect(request.META['HTTP_REFERER'])
    else:
        comment_form = CommentForm()
    context['comment_form'] = comment_form

    return render(request, 'blog/blog_detail.html', context)


def blog_list(request, lang=None, drupal_blogs_alias_url=None, drupal_uid=None):
    lang = request.LANGUAGE_CODE

    blogs = Blog.objects.language(lang).filter(is_active=True, 
        front_page=True).annotate(comment_count=Count('comment', distinct=True),
        tags_count=Count('tags', distinct=True)).order_by('-on_top', '-create_time')

    if drupal_blogs_alias_url:
        blogs = blogs.filter(user__drupal_blogs_alias_url=drupal_blogs_alias_url)
    elif drupal_uid:
        blogs = blogs.filter(user__drupal_uid=drupal_uid)

    paginator = Paginator(blogs, 30)
    page = request.GET.get('p', request.GET.get('page'))
    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)

    page_name = ''
    if request.get_full_path() != '/':
        page_name = ' | blogs'

    context = {'content': content, 'page_title': page_name}

    return render(request, 'blog/blog_list.html', context)


#@ajax_navigation
def tags(request, tag=None):
    lang = request.LANGUAGE_CODE

    if tag:
        context = Blog.objects.language(lang).filter(tags__slug__in=[tag])\
            .annotate(comment_count=Count('comment', distinct=True),
            tags_count=Count('tags', distinct=True)).order_by('-on_top', '-create_time')
    else:
        context = Tag.objects.all()
        return render(request, 'tag_list.html', {'content': context})

    if not context:
        return render(request, 'blog/blog_list.html', {'content': context})
    paginator = Paginator(context, 10)

    page = request.GET.get('p')
    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)

    last_date = content[0].create_time.date()
    for c in content:
        content[content.index(c) - 1].__setattr__('linebreack',
                            (c.create_time.date() != last_date))
        if c.create_time.date() != last_date:
            content[content.index(c) - 1].__setattr__('post_date', last_date)
        last_date = c.create_time.date()
    content[-1].__setattr__('post_date', last_date)
    content[-1].__setattr__('linebreack', True)
    return render(request, 'blog/blog_list.html', {'content': content})
