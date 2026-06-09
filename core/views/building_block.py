from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from core.models import BuildingBlock, Language


def _validate(post):
    values = {
        'content': post.get('content', '').strip(),
        'language_id': post.get('language_id', '').strip(),
        'usage': post.get('usage', '').strip(),
    }
    errors = {}
    if not values['content']:
        errors['content'] = 'Required.'
    if not values['language_id']:
        errors['language_id'] = 'Required.'
    elif not Language.objects.filter(iso3=values['language_id']).exists():
        errors['language_id'] = 'Select a valid language.'
    if not values['usage']:
        errors['usage'] = 'Required.'
    return values, errors


def _languages():
    return Language.objects.order_by('name')


def building_block_list(request):
    building_blocks = BuildingBlock.objects.select_related('language').order_by('language_id', 'id')
    return render(request, 'core/building_block/list.html', {'building_blocks': building_blocks})


def building_block_create(request):
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            obj = BuildingBlock.objects.create(**values)
            return redirect('core:building_block_detail', pk=obj.pk)
        return render(request, 'core/building_block/form.html', {'values': values, 'errors': errors, 'languages': _languages()})
    return render(request, 'core/building_block/form.html', {'languages': _languages()})


def building_block_detail(request, pk):
    obj = get_object_or_404(BuildingBlock, pk=pk)
    return render(request, 'core/building_block/detail.html', {'obj': obj})


def building_block_update(request, pk):
    obj = get_object_or_404(BuildingBlock, pk=pk)
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            obj.content = values['content']
            obj.language_id = values['language_id']
            obj.usage = values['usage']
            obj.save()
            return redirect('core:building_block_detail', pk=obj.pk)
        return render(request, 'core/building_block/form.html', {'values': values, 'errors': errors, 'obj': obj, 'languages': _languages()})
    values = {
        'content': obj.content,
        'language_id': obj.language_id,
        'usage': obj.usage,
    }
    return render(request, 'core/building_block/form.html', {'values': values, 'obj': obj, 'languages': _languages()})


def building_block_delete(request, pk):
    obj = get_object_or_404(BuildingBlock, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('core:building_block_list')
    return render(request, 'core/building_block/confirm_delete.html', {'obj': obj})


def building_block_json(request, pk):
    obj = get_object_or_404(BuildingBlock, pk=pk)
    return JsonResponse({
        'id': obj.pk,
        'content': obj.content,
        'usage': obj.usage,
        'language_id': obj.language_id,
    })


def building_block_practice(request):
    return render(request, 'core/building_block/practice.html', {})
