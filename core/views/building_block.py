import re

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from core.models import BuildingBlock


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


def building_block_list(request):
    building_blocks = BuildingBlock.objects.all().order_by('language_code', 'id')
    return render(request, 'core/building_block/list.html', {'building_blocks': building_blocks})


def building_block_create(request):
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            obj = BuildingBlock.objects.create(**values)
            return redirect('core:building_block_detail', pk=obj.pk)
        return render(request, 'core/building_block/form.html', {'values': values, 'errors': errors})
    return render(request, 'core/building_block/form.html', {})


def building_block_detail(request, pk):
    obj = get_object_or_404(BuildingBlock, pk=pk)
    return render(request, 'core/building_block/detail.html', {'obj': obj})


def building_block_update(request, pk):
    obj = get_object_or_404(BuildingBlock, pk=pk)
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            obj.content = values['content']
            obj.language_code = values['language_code']
            obj.usage = values['usage']
            obj.save()
            return redirect('core:building_block_detail', pk=obj.pk)
        return render(request, 'core/building_block/form.html', {'values': values, 'errors': errors, 'obj': obj})
    values = {
        'content': obj.content,
        'language_code': obj.language_code,
        'usage': obj.usage,
    }
    return render(request, 'core/building_block/form.html', {'values': values, 'obj': obj})


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
        'language_code': obj.language_code,
    })


def building_block_practice(request):
    return render(request, 'core/building_block/practice.html', {})
