from django.shortcuts import get_object_or_404, redirect, render

from core.models import Dialog, Situation


def _validate(post):
    errors = {}
    if not post.get('situation', '').strip():
        errors['situation'] = 'Required.'
    if not post.get('name', '').strip():
        errors['name'] = 'Required.'
    values = {
        'name': post.get('name', '').strip(),
        'speakers_raw': post.get('speakers_raw', '').strip(),
    }
    return values, errors


def _parse_speakers(raw):
    return [line.strip() for line in raw.splitlines() if line.strip()]


def _build_mermaid(dialog):
    nodes = list(dialog.nodes.prefetch_related('utterances__speech_act', 'utterances__next_node'))
    if not nodes:
        return ''
    lines = ['flowchart TD']
    node_ids = {n.pk for n in nodes}
    end_counter = 0
    for node in nodes:
        start_marker = ' ◀' if dialog.start_node_id == node.pk else ''
        lines.append(f'  N{node.pk}["{node.speaker}{start_marker}"]')
        for u in node.utterances.all():
            sa = u.speech_act.description[:25].replace('"', "'")
            if u.next_node_id and u.next_node_id in node_ids:
                lines.append(f'  N{node.pk} -->|"{sa}"| N{u.next_node_id}')
            else:
                end_counter += 1
                lines.append(f'  END{end_counter}(( ))')
                lines.append(f'  N{node.pk} -->|"{sa}"| END{end_counter}')
    return '\n'.join(lines)


def dialog_list(request):
    dialogs = Dialog.objects.select_related('situation').order_by('id')
    return render(request, 'core/dialog/list.html', {'dialogs': dialogs})


def dialog_create(request):
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            situation = get_object_or_404(Situation, pk=request.POST['situation'])
            obj = Dialog.objects.create(
                situation=situation,
                name=values['name'],
                speakers=_parse_speakers(values['speakers_raw']),
            )
            return redirect('core:dialog_detail', pk=obj.pk)
        return render(request, 'core/dialog/form.html', {
            'values': values,
            'errors': errors,
            'situations': Situation.objects.all().order_by('id'),
            'selected_situation': request.POST.get('situation', ''),
        })
    return render(request, 'core/dialog/form.html', {
        'situations': Situation.objects.all().order_by('id'),
        'selected_situation': request.GET.get('situation', ''),
    })


def dialog_detail(request, pk):
    obj = get_object_or_404(
        Dialog.objects.select_related('situation').prefetch_related(
            'nodes__utterances__speech_act',
            'nodes__utterances__next_node',
            'nodes__utterances__lines__sentence',
        ),
        pk=pk,
    )
    return render(request, 'core/dialog/detail.html', {
        'obj': obj,
        'mermaid_src': _build_mermaid(obj),
    })


def dialog_update(request, pk):
    obj = get_object_or_404(Dialog, pk=pk)
    nodes = obj.nodes.all()
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            situation = get_object_or_404(Situation, pk=request.POST['situation'])
            obj.situation = situation
            obj.name = values['name']
            obj.speakers = _parse_speakers(values['speakers_raw'])
            start_node_id = request.POST.get('start_node') or None
            obj.start_node_id = start_node_id
            obj.save()
            return redirect('core:dialog_detail', pk=obj.pk)
        return render(request, 'core/dialog/form.html', {
            'values': values,
            'errors': errors,
            'obj': obj,
            'nodes': nodes,
            'situations': Situation.objects.all().order_by('id'),
            'selected_situation': request.POST.get('situation', ''),
            'selected_start_node': request.POST.get('start_node', ''),
        })
    values = {
        'name': obj.name,
        'speakers_raw': '\n'.join(obj.speakers),
    }
    return render(request, 'core/dialog/form.html', {
        'values': values,
        'obj': obj,
        'nodes': nodes,
        'situations': Situation.objects.all().order_by('id'),
        'selected_situation': str(obj.situation_id),
        'selected_start_node': str(obj.start_node_id) if obj.start_node_id else '',
    })


def dialog_delete(request, pk):
    obj = get_object_or_404(Dialog, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('core:dialog_list')
    return render(request, 'core/dialog/confirm_delete.html', {'obj': obj})
