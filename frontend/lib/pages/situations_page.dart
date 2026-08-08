import 'package:flutter/material.dart';

import '../models/situation.dart';
import '../services/api_client.dart';
import '../services/interest_prefs.dart';
import '../services/situations_repository.dart';
import '../widgets/situation_list_item.dart';

class SituationsPage extends StatefulWidget {
  final SituationsRepository repository;
  final InterestPrefs interestPrefs;

  const SituationsPage({
    super.key,
    this.repository = const SituationsRepository(),
    this.interestPrefs = const InterestPrefs(),
  });

  @override
  State<SituationsPage> createState() => _SituationsPageState();
}

class _SituationsPageState extends State<SituationsPage> {
  late Future<List<LanguageGroup>> _groupsFuture;
  Set<int> _interestedIds = {};

  @override
  void initState() {
    super.initState();
    _load();
  }

  void _load() {
    _groupsFuture = widget.repository.fetchGrouped();
    widget.interestPrefs.getInterestedIds().then((ids) {
      if (mounted) setState(() => _interestedIds = ids);
    });
  }

  Future<void> _toggle(int situationId, bool interested) async {
    await widget.interestPrefs.setInterested(situationId, interested);
    setState(() {
      if (interested) {
        _interestedIds.add(situationId);
      } else {
        _interestedIds.remove(situationId);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Situations')),
      body: FutureBuilder<List<LanguageGroup>>(
        future: _groupsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState != ConnectionState.done) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            final message = snapshot.error is ApiException
                ? (snapshot.error as ApiException).message
                : 'Something went wrong.';
            return Center(child: Text('Failed to load situations: $message'));
          }
          final groups = snapshot.data ?? [];
          if (groups.isEmpty) {
            return const Center(child: Text('No situations available yet.'));
          }
          return ListView(
            children: [
              for (final group in groups) ...[
                Padding(
                  padding: const EdgeInsets.fromLTRB(16, 16, 16, 4),
                  child: Text(
                    group.language,
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                ),
                for (final situation in group.situations)
                  SituationListItem(
                    situation: situation,
                    interested: _interestedIds.contains(situation.id),
                    onChanged: (value) => _toggle(situation.id, value),
                  ),
              ],
            ],
          );
        },
      ),
    );
  }
}
