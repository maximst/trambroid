from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .forms import ProfileForm


User = get_user_model()


def profile(request, username=None):
    if username:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = get_object_or_404(User, drupal_uid=username)
    else:
        user = request.user

    can_edit = (user == request.user and user.is_authenticated)

    context = {'profile_user': user, 'page_title': ' | %s' % user}

    if can_edit:
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                return redirect(request.get_full_path(), '/')
        else:
            form = ProfileForm(instance=user)

        context['form'] = form

    return render(request, 'registration/profile_form.html', context)
