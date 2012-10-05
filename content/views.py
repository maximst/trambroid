# -*-coding: utf8-*-
from django.http import Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from models import Blog

def blog_detail(request, slug):
    try:
        content = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        return Http404()
    contents = {'content': content}
    contents.update(csrf(request))
    return render_to_response('blog/blog_detail.html', contents,
                              context_instance=RequestContext(request))


def blog_list(request):
    contents = Blog.objects.all()
    return render_to_response('blog/blog_list.html', {'content': contents},
                              context_instance=RequestContext(request))
