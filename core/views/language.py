import re

from django.shortcuts import get_object_or_404, redirect, render

from core.models import Language


def _validate(post, current_pk=None):
    values = {
        'iso3': post.get('iso3', '').strip().lower(),
        'name': post.get('name', '').strip(),
    }
    errors = {}
    if not re.fullmatch(r'[a-zA-Z]{3}', values['iso3']):
        errors['iso3'] = 'Must be exactly 3 alphabetic characters.'
    elif Language.objects.filter(iso3=values['iso3']).exclude(iso3=current_pk).exists():
        errors['iso3'] = 'A language with this code already exists.'
    if not values['name']:
        errors['name'] = 'Required.'
    return values, errors


def language_list(request):
    languages = Language.objects.all().order_by('name')
    return render(request, 'core/language/list.html', {'languages': languages})


def language_create(request):
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            obj = Language.objects.create(**values)
            return redirect('core:language_detail', pk=obj.pk)
        return render(request, 'core/language/form.html', {'values': values, 'errors': errors})
    return render(request, 'core/language/form.html', {})


def language_detail(request, pk):
    obj = get_object_or_404(Language, pk=pk)
    return render(request, 'core/language/detail.html', {'obj': obj})


def language_update(request, pk):
    obj = get_object_or_404(Language, pk=pk)
    if request.method == 'POST':
        values, errors = _validate(request.POST, current_pk=pk)
        if not errors:
            new_pk = values['iso3']
            obj.name = values['name']
            if new_pk != pk:
                Language.objects.create(iso3=new_pk, name=values['name'])
                obj.building_blocks.update(language_id=new_pk)
                obj.sentences.update(language_id=new_pk)
                obj.situations.update(language_id=new_pk)
                obj.delete()
                return redirect('core:language_detail', pk=new_pk)
            obj.save()
            return redirect('core:language_detail', pk=obj.pk)
        return render(request, 'core/language/form.html', {'values': values, 'errors': errors, 'obj': obj})
    values = {'iso3': obj.iso3, 'name': obj.name}
    return render(request, 'core/language/form.html', {'values': values, 'obj': obj})


def language_delete(request, pk):
    obj = get_object_or_404(Language, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('core:language_list')
    return render(request, 'core/language/confirm_delete.html', {'obj': obj})
