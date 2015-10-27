#-*- coding: utf-8 -*-
from django import forms
from models import Comment

class CommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea, label="Add a comment")
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)

    def save(self, blog=None, user=None, ip='127.0.0.1', language='ru'):
        if self.cleaned_data['body'] and blog and user:
            parent = self.cleaned_data.get('parent') or None
            comment = Comment.objects.create(body=self.cleaned_data['body'],
                                        parent_id=parent, blog=blog, user=user,
                                        language=language, ip=ip)