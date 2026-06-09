from django.shortcuts import get_object_or_404, redirect, render

from core.models import DialogNode, DialogUtterance, SpeechAct


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
    node_id = request.POST.get('node') or request.GET.get('node', '')
    node = get_object_or_404(DialogNode.objects.select_related('dialog'), pk=node_id)
    dialog = node.dialog
    dialog_nodes = dialog.nodes.all()

    if request.method == 'POST':
        errors = {}
        if not request.POST.get('speech_act_text', '').strip():
            errors['speech_act'] = 'Required.'
        if not errors:
            speech_act = _resolve_speech_act(request.POST)
            next_node_id = request.POST.get('next_node') or None
            DialogUtterance.objects.create(
                node=node,
                speech_act=speech_act,
                next_node_id=next_node_id,
            )
            return redirect('core:dialog_detail', pk=dialog.pk)
        sel = {k: request.POST.get(k, '') for k in ('speech_act_id', 'speech_act_text')}
        return render(request, 'core/dialog_utterance/form.html', {
            'node': node, 'dialog': dialog, 'dialog_nodes': dialog_nodes,
            'errors': errors,
            'initial_data': _initial_data(sel),
            'selected_next_node': request.POST.get('next_node', ''),
            'siblings': node.utterances.select_related('speech_act'),
            'predecessors': DialogUtterance.objects.filter(next_node=node).select_related('node', 'speech_act'),
        })

    return render(request, 'core/dialog_utterance/form.html', {
        'node': node, 'dialog': dialog, 'dialog_nodes': dialog_nodes,
        'initial_data': _initial_data({}),
        'siblings': node.utterances.select_related('speech_act'),
        'predecessors': DialogUtterance.objects.filter(next_node=node).select_related('node', 'speech_act'),
    })


def dialog_utterance_update(request, pk):
    obj = get_object_or_404(
        DialogUtterance.objects.select_related('node__dialog', 'speech_act', 'next_node'),
        pk=pk,
    )
    node = obj.node
    dialog = node.dialog
    dialog_nodes = dialog.nodes.all()

    if request.method == 'POST':
        errors = {}
        if not request.POST.get('speech_act_text', '').strip():
            errors['speech_act'] = 'Required.'
        if not errors:
            speech_act = _resolve_speech_act(request.POST)
            next_node_id = request.POST.get('next_node') or None
            obj.speech_act = speech_act
            obj.next_node_id = next_node_id
            obj.save()
            return redirect('core:dialog_detail', pk=dialog.pk)
        sel = {k: request.POST.get(k, '') for k in ('speech_act_id', 'speech_act_text')}
        return render(request, 'core/dialog_utterance/form.html', {
            'obj': obj, 'node': node, 'dialog': dialog, 'dialog_nodes': dialog_nodes,
            'errors': errors,
            'initial_data': _initial_data(sel),
            'selected_next_node': request.POST.get('next_node', ''),
            'siblings': node.utterances.exclude(pk=obj.pk).select_related('speech_act'),
            'predecessors': DialogUtterance.objects.filter(next_node=node).select_related('node', 'speech_act'),
        })

    sel = {
        'speech_act_text': obj.speech_act.description,
        'speech_act_id': str(obj.speech_act_id),
    }
    return render(request, 'core/dialog_utterance/form.html', {
        'obj': obj, 'node': node, 'dialog': dialog, 'dialog_nodes': dialog_nodes,
        'initial_data': _initial_data(sel),
        'selected_next_node': str(obj.next_node_id) if obj.next_node_id else '',
        'siblings': node.utterances.exclude(pk=obj.pk).select_related('speech_act'),
        'predecessors': DialogUtterance.objects.filter(next_node=node).select_related('node', 'speech_act'),
    })


def dialog_utterance_delete(request, pk):
    obj = get_object_or_404(DialogUtterance.objects.select_related('node__dialog'), pk=pk)
    dialog = obj.node.dialog
    if request.method == 'POST':
        obj.delete()
        return redirect('core:dialog_detail', pk=dialog.pk)
    return render(request, 'core/dialog_utterance/confirm_delete.html', {'obj': obj, 'dialog': dialog})
