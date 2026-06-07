import re

from django.shortcuts import get_object_or_404, redirect, render

from core.models import BuildingBlock, Sentence


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


def sentence_create(request, bb_pk):
    bb = get_object_or_404(BuildingBlock, pk=bb_pk)
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            sentence = Sentence.objects.create(**values)
            bb.sentences.add(sentence)
            return redirect('core:building_block_detail', pk=bb_pk)
        return render(request, 'core/sentence/form.html', {'values': values, 'errors': errors, 'bb': bb})
    return render(request, 'core/sentence/form.html', {'bb': bb})


def sentence_update(request, bb_pk, pk):
    bb = get_object_or_404(BuildingBlock, pk=bb_pk)
    sentence = get_object_or_404(Sentence, pk=pk)
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            sentence.content = values['content']
            sentence.language_code = values['language_code']
            sentence.usage = values['usage']
            sentence.save()
            return redirect('core:building_block_detail', pk=bb_pk)
        return render(request, 'core/sentence/form.html', {'values': values, 'errors': errors, 'bb': bb, 'obj': sentence})
    values = {
        'content': sentence.content,
        'language_code': sentence.language_code,
        'usage': sentence.usage,
    }
    return render(request, 'core/sentence/form.html', {'values': values, 'bb': bb, 'obj': sentence})


def sentence_delete(request, bb_pk, pk):
    bb = get_object_or_404(BuildingBlock, pk=bb_pk)
    sentence = get_object_or_404(Sentence, pk=pk)
    if request.method == 'POST':
        sentence.delete()
        return redirect('core:building_block_detail', pk=bb_pk)
    return render(request, 'core/sentence/confirm_delete.html', {'obj': sentence, 'bb': bb})
