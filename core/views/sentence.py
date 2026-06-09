from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from core.models import Language, Sentence, Situation


def _validate(post):
    values = {
        'content': post.get('content', '').strip(),
        'language_id': post.get('language_id', '').strip(),
    }
    errors = {}
    if not values['content']:
        errors['content'] = 'Required.'
    if not values['language_id']:
        errors['language_id'] = 'Required.'
    elif not Language.objects.filter(iso3=values['language_id']).exists():
        errors['language_id'] = 'Select a valid language.'
    return values, errors


def _languages():
    return Language.objects.order_by('name')


def sentence_list(request):
    sentences = Sentence.objects.select_related('language').order_by('language_id', 'id')
    return render(request, 'core/sentence/list.html', {'sentences': sentences})


def sentence_create(request):
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            obj = Sentence.objects.create(**values)
            return redirect('core:sentence_detail', pk=obj.pk)
        return render(request, 'core/sentence/form.html', {'values': values, 'errors': errors, 'languages': _languages()})
    return render(request, 'core/sentence/form.html', {'languages': _languages()})


def sentence_detail(request, pk):
    obj = get_object_or_404(Sentence, pk=pk)
    return render(request, 'core/sentence/detail.html', {'obj': obj})


def sentence_update(request, pk):
    obj = get_object_or_404(Sentence, pk=pk)
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            obj.content = values['content']
            obj.language_id = values['language_id']
            obj.save()
            return redirect('core:sentence_detail', pk=obj.pk)
        return render(request, 'core/sentence/form.html', {'values': values, 'errors': errors, 'obj': obj, 'languages': _languages()})
    values = {'content': obj.content, 'language_id': obj.language_id}
    return render(request, 'core/sentence/form.html', {'values': values, 'obj': obj, 'languages': _languages()})


def sentence_delete(request, pk):
    obj = get_object_or_404(Sentence, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('core:sentence_list')
    return render(request, 'core/sentence/confirm_delete.html', {'obj': obj})


def sentence_search(request):
    q = request.GET.get('q', '').strip()
    situation_id = request.GET.get('situation', '').strip()
    qs = Sentence.objects.all()
    if situation_id:
        try:
            situation = Situation.objects.get(pk=situation_id)
            if situation.language_id:
                qs = qs.filter(language_id=situation.language_id)
        except Situation.DoesNotExist:
            pass
    if q:
        qs = qs.filter(content__icontains=q)
    results = [{'id': s.pk, 'label': s.content} for s in qs[:10]]
    return JsonResponse(results, safe=False)
