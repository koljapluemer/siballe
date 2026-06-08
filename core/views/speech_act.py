from django.shortcuts import get_object_or_404, redirect, render

from core.models import Sentence, Situation, SpeechAct


def _validate(post):
    values = {'description': post.get('description', '').strip()}
    errors = {}
    if not values['description']:
        errors['description'] = 'Required.'
    return values, errors


def speech_act_create(request, situation_pk):
    situation = get_object_or_404(Situation, pk=situation_pk)
    all_sentences = Sentence.objects.all().order_by('language_code', 'id')
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        sentence_ids = request.POST.getlist('sentences')
        if not errors:
            obj = SpeechAct.objects.create(description=values['description'], situation=situation)
            obj.sentences.set(Sentence.objects.filter(pk__in=sentence_ids))
            return redirect('core:situation_detail', pk=situation_pk)
        return render(request, 'core/speech_act/form.html', {
            'values': values, 'errors': errors,
            'situation': situation, 'all_sentences': all_sentences,
            'selected_ids': [int(i) for i in sentence_ids if i.isdigit()],
        })
    return render(request, 'core/speech_act/form.html', {
        'situation': situation, 'all_sentences': all_sentences, 'selected_ids': [],
    })


def speech_act_update(request, situation_pk, pk):
    situation = get_object_or_404(Situation, pk=situation_pk)
    obj = get_object_or_404(SpeechAct, pk=pk)
    all_sentences = Sentence.objects.all().order_by('language_code', 'id')
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        sentence_ids = request.POST.getlist('sentences')
        if not errors:
            obj.description = values['description']
            obj.save()
            obj.sentences.set(Sentence.objects.filter(pk__in=sentence_ids))
            return redirect('core:situation_detail', pk=situation_pk)
        return render(request, 'core/speech_act/form.html', {
            'values': values, 'errors': errors, 'obj': obj,
            'situation': situation, 'all_sentences': all_sentences,
            'selected_ids': [int(i) for i in sentence_ids if i.isdigit()],
        })
    values = {'description': obj.description}
    selected_ids = list(obj.sentences.values_list('pk', flat=True))
    return render(request, 'core/speech_act/form.html', {
        'values': values, 'obj': obj,
        'situation': situation, 'all_sentences': all_sentences,
        'selected_ids': selected_ids,
    })


def speech_act_delete(request, situation_pk, pk):
    situation = get_object_or_404(Situation, pk=situation_pk)
    obj = get_object_or_404(SpeechAct, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('core:situation_detail', pk=situation_pk)
    return render(request, 'core/speech_act/confirm_delete.html', {'obj': obj, 'situation': situation})
