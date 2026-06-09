from django.shortcuts import get_object_or_404, redirect, render

from core.models import Sentence, Situation, SituationalUtterance, SpeechAct


def _validate(post):
    errors = {}
    if not post.get('situation', '').strip():
        errors['situation'] = 'Required.'
    if not post.get('speech_act_text', '').strip():
        errors['speech_act'] = 'Required.'
    if not post.get('sentence_text', '').strip():
        errors['sentence'] = 'Required.'
    values = {'context': post.get('context', '').strip()}
    return values, errors


def _resolve_speech_act(post):
    sa_id = post.get('speech_act_id', '').strip()
    sa_text = post.get('speech_act_text', '').strip()
    if sa_id:
        return get_object_or_404(SpeechAct, pk=sa_id)
    sa, _ = SpeechAct.objects.get_or_create(description=sa_text)
    return sa


def _resolve_sentence(post, situation):
    sn_id = post.get('sentence_id', '').strip()
    sn_text = post.get('sentence_text', '').strip()
    if sn_id:
        return get_object_or_404(Sentence, pk=sn_id), None
    if not situation.language_id:
        return None, 'The selected situation has no language — cannot auto-create a sentence.'
    sn, _ = Sentence.objects.get_or_create(content=sn_text, language_id=situation.language_id)
    return sn, None


def _initial_data(sel):
    return {
        'situationId': sel.get('situation', ''),
        'saText': sel.get('speech_act_text', ''),
        'saId': sel.get('speech_act_id', ''),
        'snText': sel.get('sentence_text', ''),
        'snId': sel.get('sentence_id', ''),
    }


def situational_utterance_list(request):
    utterances = SituationalUtterance.objects.select_related(
        'situation', 'speech_act', 'sentence'
    ).order_by('id')
    return render(request, 'core/situational_utterance/list.html', {'utterances': utterances})


def situational_utterance_create(request):
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            situation = get_object_or_404(Situation, pk=request.POST['situation'])
            speech_act = _resolve_speech_act(request.POST)
            sentence, err = _resolve_sentence(request.POST, situation)
            if err:
                errors['sentence'] = err
            else:
                obj = SituationalUtterance.objects.create(
                    context=values['context'],
                    situation=situation,
                    speech_act=speech_act,
                    sentence=sentence,
                )
                return redirect('core:situational_utterance_detail', pk=obj.pk)
        sel = {k: request.POST.get(k, '') for k in
               ('situation', 'speech_act_id', 'speech_act_text', 'sentence_id', 'sentence_text')}
        return render(request, 'core/situational_utterance/form.html', {
            'values': values, 'errors': errors,
            'situations': Situation.objects.all().order_by('id'),
            'initial_data': _initial_data(sel),
        })
    sel = {k: request.GET.get(k, '') for k in ('situation',)}
    return render(request, 'core/situational_utterance/form.html', {
        'situations': Situation.objects.all().order_by('id'),
        'initial_data': _initial_data(sel),
    })


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
            situation = get_object_or_404(Situation, pk=request.POST['situation'])
            speech_act = _resolve_speech_act(request.POST)
            sentence, err = _resolve_sentence(request.POST, situation)
            if err:
                errors['sentence'] = err
            else:
                obj.context = values['context']
                obj.situation = situation
                obj.speech_act = speech_act
                obj.sentence = sentence
                obj.save()
                return redirect('core:situational_utterance_detail', pk=obj.pk)
        sel = {k: request.POST.get(k, '') for k in
               ('situation', 'speech_act_id', 'speech_act_text', 'sentence_id', 'sentence_text')}
        return render(request, 'core/situational_utterance/form.html', {
            'values': values, 'errors': errors, 'obj': obj,
            'situations': Situation.objects.all().order_by('id'),
            'initial_data': _initial_data(sel),
        })
    sel = {
        'situation': str(obj.situation_id),
        'speech_act_text': obj.speech_act.description,
        'speech_act_id': str(obj.speech_act_id),
        'sentence_text': obj.sentence.content,
        'sentence_id': str(obj.sentence_id),
    }
    return render(request, 'core/situational_utterance/form.html', {
        'values': {'context': obj.context},
        'obj': obj,
        'situations': Situation.objects.all().order_by('id'),
        'initial_data': _initial_data(sel),
    })


def situational_utterance_delete(request, pk):
    obj = get_object_or_404(SituationalUtterance, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('core:situational_utterance_list')
    return render(request, 'core/situational_utterance/confirm_delete.html', {'obj': obj})
