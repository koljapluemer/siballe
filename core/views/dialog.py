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


def _md(text):
    return text.replace('`', "'").replace('"', "'")


def _build_mermaid(dialog):
    utterances = list(
        dialog.utterances
        .select_related('speech_act', 'previous_utterance')
        .prefetch_related('lines__sentence')
        .order_by('pk')
    )
    if not utterances:
        return ''
    utt_ids = {u.pk for u in utterances}
    lines = ['flowchart TD']
    end_counter = 0
    roots = [u for u in utterances if u.previous_utterance_id is None]
    non_roots = [u for u in utterances if u.previous_utterance_id is not None]

    for u in utterances:
        start_marker = ' ◀' if dialog.start_utterance_id == u.pk else ''
        parts = [f'**{_md(u.speaker)}{start_marker}**', f'*{_md(u.speech_act.description)}*']
        for ln in sorted(u.lines.all(), key=lambda l: l.order):
            parts.append(_md(ln.sentence.content))
        label = '\n'.join(parts)
        lines.append(f'  U{u.pk}["`{label}`"]')

    for u in non_roots:
        if u.previous_utterance_id in utt_ids:
            lines.append(f'  U{u.previous_utterance_id} --> U{u.pk}')

    if not non_roots and roots:
        for u in roots:
            end_counter += 1
            lines.append(f'  END{end_counter}(( ))')
            lines.append(f'  U{u.pk} --> END{end_counter}')

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
            'utterances__speech_act',
            'utterances__previous_utterance',
            'utterances__lines__sentence',
        ),
        pk=pk,
    )
    return render(request, 'core/dialog/detail.html', {
        'obj': obj,
        'mermaid_src': _build_mermaid(obj),
    })


def dialog_update(request, pk):
    obj = get_object_or_404(Dialog, pk=pk)
    utterances = obj.utterances.select_related('speech_act').order_by('pk')
    if request.method == 'POST':
        values, errors = _validate(request.POST)
        if not errors:
            situation = get_object_or_404(Situation, pk=request.POST['situation'])
            obj.situation = situation
            obj.name = values['name']
            obj.speakers = _parse_speakers(values['speakers_raw'])
            start_utterance_id = request.POST.get('start_utterance') or None
            obj.start_utterance_id = start_utterance_id
            obj.save()
            return redirect('core:dialog_detail', pk=obj.pk)
        return render(request, 'core/dialog/form.html', {
            'values': values,
            'errors': errors,
            'obj': obj,
            'utterances': utterances,
            'situations': Situation.objects.all().order_by('id'),
            'selected_situation': request.POST.get('situation', ''),
            'selected_start_utterance': request.POST.get('start_utterance', ''),
        })
    values = {
        'name': obj.name,
        'speakers_raw': '\n'.join(obj.speakers),
    }
    return render(request, 'core/dialog/form.html', {
        'values': values,
        'obj': obj,
        'utterances': utterances,
        'situations': Situation.objects.all().order_by('id'),
        'selected_situation': str(obj.situation_id),
        'selected_start_utterance': str(obj.start_utterance_id) if obj.start_utterance_id else '',
    })


def dialog_delete(request, pk):
    obj = get_object_or_404(Dialog, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('core:dialog_list')
    return render(request, 'core/dialog/confirm_delete.html', {'obj': obj})
