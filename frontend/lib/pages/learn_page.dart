import 'dart:async';
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:fsrs/fsrs.dart' as fsrs;

import '../services/db/local_exercise_store.dart';
import '../services/exercise_picking/default_exercise_picking_strategy.dart';
import '../services/exercise_picking/exercise_picking_strategy.dart';
import '../services/interest_prefs.dart';
import '../services/sync_service.dart';
import '../widgets/flashcard.dart';
import '../widgets/fsrs_button_row.dart';

enum _Stage { loading, empty, noCandidates, front, revealed }

class LearnPage extends StatefulWidget {
  final InterestPrefs interestPrefs;
  final ExercisePickingStrategy pickingStrategy;
  final LocalExerciseStore exerciseStore;
  final SyncService syncService;

  LearnPage({
    super.key,
    this.interestPrefs = const InterestPrefs(),
    this.pickingStrategy = const DefaultExercisePickingStrategy(),
    LocalExerciseStore? exerciseStore,
    SyncService? syncService,
  }) : exerciseStore = exerciseStore ?? localExerciseStore,
       syncService = syncService ?? SyncService();

  @override
  State<LearnPage> createState() => _LearnPageState();
}

class _LearnPageState extends State<LearnPage> {
  _Stage _stage = _Stage.loading;
  ExerciseCandidate? _candidate;
  final _random = Random();
  final _scheduler = fsrs.Scheduler();

  @override
  void initState() {
    super.initState();
    _loadThenSync();
  }

  /// Renders instantly from whatever is already cached locally, then
  /// refreshes in the background — the point of offline-first is that the
  /// first render never waits on the network.
  Future<void> _loadThenSync() async {
    await _startRound();
    final ids = await widget.interestPrefs.getInterestedIds();
    await widget.syncService.syncAll(interestedSituationIds: ids);
    await _startRound();
  }

  Future<void> _startRound() async {
    final ids = await widget.interestPrefs.getInterestedIds();
    if (ids.isEmpty) {
      if (mounted) setState(() => _stage = _Stage.empty);
      return;
    }

    final candidates = await widget.exerciseStore.candidatesForSituations(ids);
    final picked = widget.pickingStrategy.pick(candidates, DateTime.now().toUtc(), _random);
    if (mounted) {
      setState(() {
        _candidate = picked;
        _stage = picked == null ? _Stage.noCandidates : _Stage.front;
      });
    }
  }

  void _reveal() => setState(() => _stage = _Stage.revealed);

  Future<void> _rate(fsrs.Rating rating) async {
    final candidate = _candidate;
    if (candidate == null) return;

    final card = candidate.card ?? fsrs.Card(cardId: candidate.exercise.id);
    final result = _scheduler.reviewCard(card, rating);
    await widget.exerciseStore.saveReview(candidate.exercise.id, result.card);

    unawaited(
      widget.interestPrefs.getInterestedIds().then(
        (ids) => widget.syncService.syncAll(interestedSituationIds: ids),
      ),
    );

    await _startRound();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Learn')),
      body: Center(child: _buildBody()),
    );
  }

  Widget _buildBody() {
    switch (_stage) {
      case _Stage.loading:
        return const CircularProgressIndicator();
      case _Stage.empty:
        return Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text(
                "You haven't marked any situations to learn yet.",
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),
              ElevatedButton(onPressed: _startRound, child: const Text('Retry')),
            ],
          ),
        );
      case _Stage.noCandidates:
        return Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text(
                'No exercises are available for your situations yet.',
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),
              ElevatedButton(onPressed: _loadThenSync, child: const Text('Retry')),
            ],
          ),
        );
      case _Stage.front:
        return SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Flashcard(front: _candidate!.exercise.front),
              ElevatedButton(onPressed: _reveal, child: const Text('Reveal')),
            ],
          ),
        );
      case _Stage.revealed:
        return SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Flashcard(
                front: _candidate!.exercise.front,
                back: _candidate!.exercise.back,
                credits: _candidate!.exercise.credits,
              ),
              const SizedBox(height: 16),
              FsrsButtonRow(onRate: _rate),
              const SizedBox(height: 16),
            ],
          ),
        );
    }
  }
}
