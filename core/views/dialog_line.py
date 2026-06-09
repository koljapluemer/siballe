from django.shortcuts import get_object_or_404, redirect, render

from core.models import DialogLine, DialogUtterance, Sentence


def _resolve_sentence(post, utterance):
    sn_id = post.get('sentence_id', '').strip()
    sn_text = post.get('sentence_text', '').strip()
    if sn_id:
        return get_object_or_404(Sentence, pk=sn_id), None
    language_id = utterance.node.dialog.situation.language_id
    if not language_id:
        return None, "The dialog's situation has no language — cannot auto-create a sentence."
    sn, _ = Sentence.objects.get_or_create(content=sn_text, language_id=language_id)
    return sn, None


def _initial_data(sel):
    return {
        'snText': sel.get('sentence_text', ''),
        'snId': sel.get('sentence_id', ''),
    }


def _next_order(utterance_id):
    last = DialogLine.objects.filter(utterance_id=utterance_id).order_by('-order').first()
    return (last.order + 1) if last else 0


def dialog_line_create(request):
    utterance_id = request.POST.get('utterance') or request.GET.get('utterance', '')
    utterance = get_object_or_404(
        DialogUtterance.objects.select_related('node__dialog__situation', 'speech_act'),
        pk=utterance_id,
    )
    dialog = utterance.node.dialog

    if request.method == 'POST':
        errors = {}
        if not request.POST.get('sentence_text', '').strip():
            errors['sentence'] = 'Required.'
        order = int(request.POST.get('order', 0))
        if not errors:
            sentence, err = _resolve_sentence(request.POST, utterance)
            if err:
                errors['sentence'] = err
            else:
                context = request.POST.get('context', '').strip()
                DialogLine.objects.create(
                    utterance=utterance,
                    sentence=sentence,
                    context=context,
                    order=order,
                )
                return redirect('core:dialog_detail', pk=dialog.pk)
        sel = {k: request.POST.get(k, '') for k in ('sentence_id', 'sentence_text')}
        return render(request, 'core/dialog_line/form.html', {
            'utterance': utterance, 'dialog': dialog,
            'errors': errors,
            'values': {'context': request.POST.get('context', ''), 'order': order},
            'initial_data': _initial_data(sel),
            'siblings': utterance.lines.select_related('sentence'),
        })

    order = _next_order(utterance.pk)
    return render(request, 'core/dialog_line/form.html', {
        'utterance': utterance, 'dialog': dialog,
        'values': {'order': order},
        'initial_data': _initial_data({}),
        'siblings': utterance.lines.select_related('sentence'),
    })


def dialog_line_update(request, pk):
    obj = get_object_or_404(
        DialogLine.objects.select_related('utterance__node__dialog__situation', 'utterance__speech_act', 'sentence'),
        pk=pk,
    )
    utterance = obj.utterance
    dialog = utterance.node.dialog

    if request.method == 'POST':
        errors = {}
        if not request.POST.get('sentence_text', '').strip():
            errors['sentence'] = 'Required.'
        order = int(request.POST.get('order', obj.order))
        if not errors:
            sentence, err = _resolve_sentence(request.POST, utterance)
            if err:
                errors['sentence'] = err
            else:
                obj.sentence = sentence
                obj.context = request.POST.get('context', '').strip()
                obj.order = order
                obj.save()
                return redirect('core:dialog_detail', pk=dialog.pk)
        sel = {k: request.POST.get(k, '') for k in ('sentence_id', 'sentence_text')}
        return render(request, 'core/dialog_line/form.html', {
            'obj': obj, 'utterance': utterance, 'dialog': dialog,
            'errors': errors,
            'values': {'context': request.POST.get('context', ''), 'order': order},
            'initial_data': _initial_data(sel),
            'siblings': utterance.lines.exclude(pk=obj.pk).select_related('sentence'),
        })

    sel = {
        'sentence_text': obj.sentence.content,
        'sentence_id': str(obj.sentence_id),
    }
    return render(request, 'core/dialog_line/form.html', {
        'obj': obj, 'utterance': utterance, 'dialog': dialog,
        'values': {'context': obj.context, 'order': obj.order},
        'initial_data': _initial_data(sel),
        'siblings': utterance.lines.exclude(pk=obj.pk).select_related('sentence'),
    })


def dialog_line_delete(request, pk):
    obj = get_object_or_404(DialogLine.objects.select_related('utterance__node__dialog'), pk=pk)
    dialog = obj.utterance.node.dialog
    if request.method == 'POST':
        obj.delete()
        return redirect('core:dialog_detail', pk=dialog.pk)
    return render(request, 'core/dialog_line/confirm_delete.html', {'obj': obj, 'dialog': dialog})
