from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from core.models import SpeechAct


def _validate(post):
    values = {'description': post.get('description', '').strip()}
    errors = {}
    if not values['description']:
        errors['description'] = 'Required.'
    return values, errors


def speech_act_list(request):
    speech_acts = SpeechAct.objects.all().order_by('id')
    return render(request, 'core/speech_act/list.html', {'speech_acts': speech_acts})


def speech_act_create(request):
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            obj = SpeechAct.objects.create(**values)
            return redirect('core:speech_act_detail', pk=obj.pk)
        return render(request, 'core/speech_act/form.html', {'values': values, 'errors': errors})
    return render(request, 'core/speech_act/form.html', {})


def speech_act_detail(request, pk):
    obj = get_object_or_404(SpeechAct, pk=pk)
    return render(request, 'core/speech_act/detail.html', {'obj': obj})


def speech_act_update(request, pk):
    obj = get_object_or_404(SpeechAct, pk=pk)
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            obj.description = values['description']
            obj.save()
            return redirect('core:speech_act_detail', pk=obj.pk)
        return render(request, 'core/speech_act/form.html', {'values': values, 'errors': errors, 'obj': obj})
    values = {'description': obj.description}
    return render(request, 'core/speech_act/form.html', {'values': values, 'obj': obj})


def speech_act_delete(request, pk):
    obj = get_object_or_404(SpeechAct, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('core:speech_act_list')
    return render(request, 'core/speech_act/confirm_delete.html', {'obj': obj})


def speech_act_search(request):
    q = request.GET.get('q', '').strip()
    qs = SpeechAct.objects.all()
    if q:
        qs = qs.filter(description__icontains=q)
    results = [{'id': sa.pk, 'label': sa.description} for sa in qs[:10]]
    return JsonResponse(results, safe=False)
