from django.shortcuts import get_object_or_404, redirect, render

from core.models import Dialog, DialogUtterance, SpeechAct


def _resolve_speech_act(post):
    sa_id = post.get('speech_act_id', '').strip()
    sa_text = post.get('speech_act_text', '').strip()
    if sa_id:
        return get_object_or_404(SpeechAct, pk=sa_id)
    sa, _ = SpeechAct.objects.get_or_create(description=sa_text)
    return sa


def _initial_data(sel):
    return {
        'saText': sel.get('speech_act_text', ''),
        'saId': sel.get('speech_act_id', ''),
    }


def dialog_utterance_create(request):
    dialog_id = request.POST.get('dialog') or request.GET.get('dialog', '')
    dialog = get_object_or_404(Dialog, pk=dialog_id)
    dialog_utterances = dialog.utterances.select_related('speech_act').order_by('pk')

    if request.method == 'POST':
        errors = {}
        speaker = request.POST.get('speaker', '').strip()
        if not speaker:
            errors['speaker'] = 'Required.'
        if not request.POST.get('speech_act_text', '').strip():
            errors['speech_act'] = 'Required.'
        if not errors:
            speech_act = _resolve_speech_act(request.POST)
            obj = DialogUtterance.objects.create(dialog=dialog, speaker=speaker, speech_act=speech_act)
            prev_ids = request.POST.getlist('previous_utterances')
            if prev_ids:
                obj.previous_utterances.set(prev_ids)
            if dialog.start_utterance_id is None:
                dialog.start_utterance = obj
                dialog.save(update_fields=['start_utterance'])
            return redirect('core:dialog_detail', pk=dialog.pk)
        sel = {k: request.POST.get(k, '') for k in ('speech_act_id', 'speech_act_text')}
        return render(request, 'core/dialog_utterance/form.html', {
            'dialog': dialog,
            'dialog_utterances': dialog_utterances,
            'errors': errors,
            'initial_data': _initial_data(sel),
            'selected_previous_utterances': request.POST.getlist('previous_utterances'),
            'values': {'speaker': speaker},
        })

    pre = request.GET.get('previous_utterance', '')
    return render(request, 'core/dialog_utterance/form.html', {
        'dialog': dialog,
        'dialog_utterances': dialog_utterances,
        'initial_data': _initial_data({}),
        'values': {},
        'selected_previous_utterances': [pre] if pre else [],
    })


def dialog_utterance_update(request, pk):
    obj = get_object_or_404(
        DialogUtterance.objects.select_related('dialog', 'speech_act'),
        pk=pk,
    )
    dialog = obj.dialog
    dialog_utterances = dialog.utterances.select_related('speech_act').order_by('pk')
    siblings = dialog_utterances.filter(
        previous_utterances__in=obj.previous_utterances.all()
    ).exclude(pk=obj.pk).distinct()
    following = dialog_utterances.filter(previous_utterances=obj)

    if request.method == 'POST':
        errors = {}
        speaker = request.POST.get('speaker', '').strip()
        if not speaker:
            errors['speaker'] = 'Required.'
        if not request.POST.get('speech_act_text', '').strip():
            errors['speech_act'] = 'Required.'
        if not errors:
            speech_act = _resolve_speech_act(request.POST)
            obj.speaker = speaker
            obj.speech_act = speech_act
            obj.save()
            obj.previous_utterances.set(request.POST.getlist('previous_utterances'))
            return redirect('core:dialog_detail', pk=dialog.pk)
        sel = {k: request.POST.get(k, '') for k in ('speech_act_id', 'speech_act_text')}
        return render(request, 'core/dialog_utterance/form.html', {
            'obj': obj, 'dialog': dialog,
            'dialog_utterances': dialog_utterances,
            'errors': errors,
            'initial_data': _initial_data(sel),
            'selected_previous_utterances': request.POST.getlist('previous_utterances'),
            'values': {'speaker': speaker},
            'siblings': siblings,
            'following': following,
        })

    sel = {
        'speech_act_text': obj.speech_act.description,
        'speech_act_id': str(obj.speech_act_id),
    }
    return render(request, 'core/dialog_utterance/form.html', {
        'obj': obj, 'dialog': dialog,
        'dialog_utterances': dialog_utterances,
        'initial_data': _initial_data(sel),
        'selected_previous_utterances': [str(p.pk) for p in obj.previous_utterances.all()],
        'values': {'speaker': obj.speaker},
        'siblings': siblings,
        'following': following,
    })


def dialog_utterance_delete(request, pk):
    obj = get_object_or_404(DialogUtterance.objects.select_related('dialog'), pk=pk)
    dialog = obj.dialog
    if request.method == 'POST':
        if dialog.start_utterance_id == obj.pk:
            dialog.start_utterance = None
            dialog.save(update_fields=['start_utterance'])
        obj.delete()
        return redirect('core:dialog_detail', pk=dialog.pk)
    return render(request, 'core/dialog_utterance/confirm_delete.html', {'obj': obj, 'dialog': dialog})
