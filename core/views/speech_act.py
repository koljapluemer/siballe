from django.shortcuts import get_object_or_404, redirect, render

from core.models import Sentence, Situation, SpeechAct


def _validate(post):
    values = {'description': post.get('description', '').strip()}
    errors = {}
    if not values['description']:
        errors['description'] = 'Required.'
    return values, errors


def speech_act_list(request):
    speech_acts = SpeechAct.objects.select_related('situation').order_by('id')
    return render(request, 'core/speech_act/list.html', {'speech_acts': speech_acts})


def speech_act_create(request):
    situations = Situation.objects.all().order_by('id')
    all_sentences = Sentence.objects.all().order_by('language_code', 'id')
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        situation_id = request.POST.get('situation', '').strip()
        sentence_ids = request.POST.getlist('sentences')
        if not situation_id:
            errors['situation'] = 'Required.'
        if not errors:
            situation = get_object_or_404(Situation, pk=situation_id)
            obj = SpeechAct.objects.create(description=values['description'], situation=situation)
            obj.sentences.set(Sentence.objects.filter(pk__in=sentence_ids))
            return redirect('core:speech_act_detail', pk=obj.pk)
        return render(request, 'core/speech_act/form.html', {
            'values': values, 'errors': errors,
            'situations': situations, 'selected_situation_id': situation_id,
            'all_sentences': all_sentences,
            'selected_ids': [int(i) for i in sentence_ids if i.isdigit()],
        })
    preselect = request.GET.get('situation', '')
    return render(request, 'core/speech_act/form.html', {
        'situations': situations, 'selected_situation_id': preselect,
        'all_sentences': all_sentences, 'selected_ids': [],
    })


def speech_act_detail(request, pk):
    obj = get_object_or_404(SpeechAct.objects.select_related('situation'), pk=pk)
    return render(request, 'core/speech_act/detail.html', {'obj': obj})


def speech_act_update(request, pk):
    obj = get_object_or_404(SpeechAct.objects.select_related('situation'), pk=pk)
    situations = Situation.objects.all().order_by('id')
    all_sentences = Sentence.objects.all().order_by('language_code', 'id')
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        situation_id = request.POST.get('situation', '').strip()
        sentence_ids = request.POST.getlist('sentences')
        if not situation_id:
            errors['situation'] = 'Required.'
        if not errors:
            situation = get_object_or_404(Situation, pk=situation_id)
            obj.description = values['description']
            obj.situation = situation
            obj.save()
            obj.sentences.set(Sentence.objects.filter(pk__in=sentence_ids))
            return redirect('core:speech_act_detail', pk=obj.pk)
        return render(request, 'core/speech_act/form.html', {
            'values': values, 'errors': errors, 'obj': obj,
            'situations': situations, 'selected_situation_id': situation_id,
            'all_sentences': all_sentences,
            'selected_ids': [int(i) for i in sentence_ids if i.isdigit()],
        })
    values = {'description': obj.description}
    selected_ids = list(obj.sentences.values_list('pk', flat=True))
    return render(request, 'core/speech_act/form.html', {
        'values': values, 'obj': obj,
        'situations': situations, 'selected_situation_id': str(obj.situation_id),
        'all_sentences': all_sentences, 'selected_ids': selected_ids,
    })


def speech_act_delete(request, pk):
    obj = get_object_or_404(SpeechAct, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('core:speech_act_list')
    return render(request, 'core/speech_act/confirm_delete.html', {'obj': obj})
