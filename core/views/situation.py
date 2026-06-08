from django.shortcuts import get_object_or_404, redirect, render

from core.models import Situation


def _validate(post):
    values = {'description': post.get('description', '').strip()}
    errors = {}
    if not values['description']:
        errors['description'] = 'Required.'
    return values, errors


def situation_list(request):
    situations = Situation.objects.all().order_by('id')
    return render(request, 'core/situation/list.html', {'situations': situations})


def situation_create(request):
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            obj = Situation.objects.create(**values)
            return redirect('core:situation_detail', pk=obj.pk)
        return render(request, 'core/situation/form.html', {'values': values, 'errors': errors})
    return render(request, 'core/situation/form.html', {})


def situation_detail(request, pk):
    obj = get_object_or_404(Situation, pk=pk)
    return render(request, 'core/situation/detail.html', {'obj': obj})


def situation_update(request, pk):
    obj = get_object_or_404(Situation, pk=pk)
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            obj.description = values['description']
            obj.save()
            return redirect('core:situation_detail', pk=obj.pk)
        return render(request, 'core/situation/form.html', {'values': values, 'errors': errors, 'obj': obj})
    values = {'description': obj.description}
    return render(request, 'core/situation/form.html', {'values': values, 'obj': obj})


def situation_delete(request, pk):
    obj = get_object_or_404(Situation, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('core:situation_list')
    return render(request, 'core/situation/confirm_delete.html', {'obj': obj})
