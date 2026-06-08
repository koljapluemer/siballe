from django.shortcuts import get_object_or_404, redirect, render

from core.models import Sentence, Situation, SituationalUtterance, SpeechAct


def _validate(post):
    values = {'context': post.get('context', '').strip()}
    errors = {}
    if not values['context']:
        errors['context'] = 'Required.'
    if not post.get('situation'):
        errors['situation'] = 'Required.'
    if not post.get('speech_act'):
        errors['speech_act'] = 'Required.'
    if not post.get('sentence'):
        errors['sentence'] = 'Required.'
    return values, errors


def _form_context(extra=None):
    ctx = {
        'situations': Situation.objects.all().order_by('id'),
        'speech_acts': SpeechAct.objects.all().order_by('id'),
        'sentences': Sentence.objects.all().order_by('language_code', 'id'),
    }
    if extra:
        ctx.update(extra)
    return ctx


def situational_utterance_list(request):
    utterances = SituationalUtterance.objects.select_related(
        'situation', 'speech_act', 'sentence'
    ).order_by('id')
    return render(request, 'core/situational_utterance/list.html', {'utterances': utterances})


def situational_utterance_create(request):
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            obj = SituationalUtterance.objects.create(
                context=values['context'],
                situation=get_object_or_404(Situation, pk=request.POST['situation']),
                speech_act=get_object_or_404(SpeechAct, pk=request.POST['speech_act']),
                sentence=get_object_or_404(Sentence, pk=request.POST['sentence']),
            )
            return redirect('core:situational_utterance_detail', pk=obj.pk)
        return render(request, 'core/situational_utterance/form.html', _form_context({
            'values': values, 'errors': errors,
            'sel': {k: request.POST.get(k, '') for k in ('situation', 'speech_act', 'sentence')},
        }))
    return render(request, 'core/situational_utterance/form.html', _form_context({'sel': {}}))


def situational_utterance_detail(request, pk):
    obj = get_object_or_404(
        SituationalUtterance.objects.select_related('situation', 'speech_act', 'sentence'), pk=pk
    )
    return render(request, 'core/situational_utterance/detail.html', {'obj': obj})


def situational_utterance_update(request, pk):
    obj = get_object_or_404(
        SituationalUtterance.objects.select_related('situation', 'speech_act', 'sentence'), pk=pk
    )
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            obj.context = values['context']
            obj.situation = get_object_or_404(Situation, pk=request.POST['situation'])
            obj.speech_act = get_object_or_404(SpeechAct, pk=request.POST['speech_act'])
            obj.sentence = get_object_or_404(Sentence, pk=request.POST['sentence'])
            obj.save()
            return redirect('core:situational_utterance_detail', pk=obj.pk)
        return render(request, 'core/situational_utterance/form.html', _form_context({
            'values': values, 'errors': errors, 'obj': obj,
            'sel': {k: request.POST.get(k, '') for k in ('situation', 'speech_act', 'sentence')},
        }))
    return render(request, 'core/situational_utterance/form.html', _form_context({
        'values': {'context': obj.context},
        'obj': obj,
        'sel': {
            'situation': str(obj.situation_id),
            'speech_act': str(obj.speech_act_id),
            'sentence': str(obj.sentence_id),
        },
    }))


def situational_utterance_delete(request, pk):
    obj = get_object_or_404(SituationalUtterance, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('core:situational_utterance_list')
    return render(request, 'core/situational_utterance/confirm_delete.html', {'obj': obj})
