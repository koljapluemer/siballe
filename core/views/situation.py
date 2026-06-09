from django.shortcuts import get_object_or_404, redirect, render

from core.models import Language, Situation


def _validate(post):
    values = {
        'description': post.get('description', '').strip(),
        'language_id': post.get('language_id', '').strip(),
    }
    errors = {}
    if not values['description']:
        errors['description'] = 'Required.'
    if not values['language_id']:
        errors['language_id'] = 'Required.'
    elif not Language.objects.filter(iso3=values['language_id']).exists():
        errors['language_id'] = 'Select a valid language.'
    return values, errors


def _languages():
    return Language.objects.order_by('name')


def situation_list(request):
    situations = Situation.objects.select_related('language').order_by('id')
    return render(request, 'core/situation/list.html', {'situations': situations})


def situation_create(request):
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            obj = Situation.objects.create(**values)
            return redirect('core:situation_detail', pk=obj.pk)
        return render(request, 'core/situation/form.html', {'values': values, 'errors': errors, 'languages': _languages()})
    return render(request, 'core/situation/form.html', {'languages': _languages()})


def situation_detail(request, pk):
    obj = get_object_or_404(Situation, pk=pk)
    return render(request, 'core/situation/detail.html', {'obj': obj})


def situation_update(request, pk):
    obj = get_object_or_404(Situation, pk=pk)
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            obj.description = values['description']
            obj.language_id = values['language_id']
            obj.save()
            return redirect('core:situation_detail', pk=obj.pk)
        return render(request, 'core/situation/form.html', {'values': values, 'errors': errors, 'obj': obj, 'languages': _languages()})
    values = {'description': obj.description, 'language_id': obj.language_id}
    return render(request, 'core/situation/form.html', {'values': values, 'obj': obj, 'languages': _languages()})


def situation_delete(request, pk):
    obj = get_object_or_404(Situation, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('core:situation_list')
    return render(request, 'core/situation/confirm_delete.html', {'obj': obj})
