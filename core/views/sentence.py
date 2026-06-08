import re

from django.shortcuts import get_object_or_404, redirect, render

from core.models import Sentence


def _validate(post):
    values = {
        'content': post.get('content', '').strip(),
        'language_code': post.get('language_code', '').strip(),
        'usage': post.get('usage', '').strip(),
    }
    errors = {}
    if not values['content']:
        errors['content'] = 'Required.'
    if not re.fullmatch(r'[a-zA-Z]{3}', values['language_code']):
        errors['language_code'] = 'Must be exactly 3 alphabetic characters.'
    if not values['usage']:
        errors['usage'] = 'Required.'
    values['language_code'] = values['language_code'].lower()
    return values, errors


def sentence_list(request):
    sentences = Sentence.objects.all().order_by('language_code', 'id')
    return render(request, 'core/sentence/list.html', {'sentences': sentences})


def sentence_create(request):
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            obj = Sentence.objects.create(**values)
            return redirect('core:sentence_detail', pk=obj.pk)
        return render(request, 'core/sentence/form.html', {'values': values, 'errors': errors})
    return render(request, 'core/sentence/form.html', {})


def sentence_detail(request, pk):
    obj = get_object_or_404(Sentence, pk=pk)
    return render(request, 'core/sentence/detail.html', {'obj': obj})


def sentence_update(request, pk):
    obj = get_object_or_404(Sentence, pk=pk)
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            obj.content = values['content']
            obj.language_code = values['language_code']
            obj.usage = values['usage']
            obj.save()
            return redirect('core:sentence_detail', pk=obj.pk)
        return render(request, 'core/sentence/form.html', {'values': values, 'errors': errors, 'obj': obj})
    values = {'content': obj.content, 'language_code': obj.language_code, 'usage': obj.usage}
    return render(request, 'core/sentence/form.html', {'values': values, 'obj': obj})


def sentence_delete(request, pk):
    obj = get_object_or_404(Sentence, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('core:sentence_list')
    return render(request, 'core/sentence/confirm_delete.html', {'obj': obj})
