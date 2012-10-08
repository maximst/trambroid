# -*-coding: utf8-*-
from django.http import Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from models import Blog

def blog_detail(request, slug):
    try:
        content = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        raise Http404()
    contents = {'content': content}
    contents.update(csrf(request))
    return render_to_response('blog/blog_detail.html', contents,
                              context_instance=RequestContext(request))


def blog_list(request, get):
    contents = Blog.objects.all()
    paginator = Paginator(contents, 30)

    page = request.GET.get('p')
    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)
    return render_to_response('blog/blog_list.html', {'content': content},
                              context_instance=RequestContext(request))
