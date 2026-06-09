from django.shortcuts import get_object_or_404, redirect, render

from core.models import Dialog, DialogNode, DialogUtterance


def dialog_node_create(request):
    dialog_id = request.POST.get('dialog') or request.GET.get('dialog', '')
    dialog = get_object_or_404(Dialog, pk=dialog_id)

    if request.method == 'POST':
        speaker = request.POST.get('speaker', '').strip()
        errors = {}
        if not speaker:
            errors['speaker'] = 'Required.'
        if not errors:
            node = DialogNode.objects.create(dialog=dialog, speaker=speaker)
            if dialog.start_node_id is None:
                dialog.start_node = node
                dialog.save(update_fields=['start_node'])
            return redirect('core:dialog_detail', pk=dialog.pk)
        return render(request, 'core/dialog_node/form.html', {
            'dialog': dialog,
            'errors': errors,
            'values': {'speaker': speaker},
        })

    return render(request, 'core/dialog_node/form.html', {'dialog': dialog})


def dialog_node_update(request, pk):
    node = get_object_or_404(DialogNode.objects.select_related('dialog'), pk=pk)
    dialog = node.dialog

    predecessors = DialogUtterance.objects.filter(next_node=node).select_related('node__dialog', 'speech_act')

    if request.method == 'POST':
        speaker = request.POST.get('speaker', '').strip()
        errors = {}
        if not speaker:
            errors['speaker'] = 'Required.'
        if not errors:
            node.speaker = speaker
            node.save()
            return redirect('core:dialog_detail', pk=dialog.pk)
        return render(request, 'core/dialog_node/form.html', {
            'obj': node,
            'dialog': dialog,
            'errors': errors,
            'values': {'speaker': speaker},
            'predecessors': predecessors,
            'utterances': node.utterances.select_related('speech_act', 'next_node'),
        })

    return render(request, 'core/dialog_node/form.html', {
        'obj': node,
        'dialog': dialog,
        'values': {'speaker': node.speaker},
        'predecessors': predecessors,
        'utterances': node.utterances.select_related('speech_act', 'next_node'),
    })


def dialog_node_delete(request, pk):
    node = get_object_or_404(DialogNode.objects.select_related('dialog'), pk=pk)
    dialog = node.dialog
    if request.method == 'POST':
        if dialog.start_node_id == node.pk:
            dialog.start_node = None
            dialog.save(update_fields=['start_node'])
        node.delete()
        return redirect('core:dialog_detail', pk=dialog.pk)
    return render(request, 'core/dialog_node/confirm_delete.html', {'obj': node, 'dialog': dialog})
