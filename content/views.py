# -*-coding: utf8-*-
from django.shortcuts import render, get_object_or_404, redirect
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from models import Blog, Comment
from forms import CommentForm

def blog_detail(request, slug):
    user = request.user

    content = get_object_or_404(Blog, slug=slug)
    comments = Comment.objects.filter(blog=content).order_by('-create_time')
    contents = {'content': content, 'comments': comments}
    contents.update(csrf(request))

    if request.method == 'POST' and user.is_authenticated():
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            ip = request.META['REMOTE_ADDR']
            comment_form.save(content, user, ip)
            return redirect(request.META['HTTP_REFERER'])
    else:
        comment_form = CommentForm()
    contents['comment_form'] = comment_form

    return render(request, 'blog/blog_detail.html', contents)


def blog_list(request):
    contents = Blog.objects.all().order_by('-create_time')
    paginator = Paginator(contents, 30)
    page = request.GET.get('p')
    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)
    return render(request, 'blog/blog_list.html', {'content': content})
