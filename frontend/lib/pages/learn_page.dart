import 'dart:math';

import 'package:flutter/material.dart';

import '../models/exercise.dart';
import '../services/api_client.dart';
import '../services/exercise_repository.dart';
import '../services/interest_prefs.dart';
import '../services/situations_repository.dart';
import '../widgets/flashcard.dart';
import '../widgets/fsrs_button_row.dart';

enum _Stage { loading, empty, front, revealed, error }

class LearnPage extends StatefulWidget {
  final SituationsRepository situationsRepository;
  final ExerciseRepository exerciseRepository;
  final InterestPrefs interestPrefs;

  const LearnPage({
    super.key,
    this.situationsRepository = const SituationsRepository(),
    this.exerciseRepository = const ExerciseRepository(),
    this.interestPrefs = const InterestPrefs(),
  });

  @override
  State<LearnPage> createState() => _LearnPageState();
}

class _LearnPageState extends State<LearnPage> {
  static const _maxRetries = 3;

  _Stage _stage = _Stage.loading;
  Exercise? _exercise;
  String? _errorMessage;
  final _random = Random();

  @override
  void initState() {
    super.initState();
    _startRound();
  }

  Future<void> _startRound() async {
    setState(() {
      _stage = _Stage.loading;
      _exercise = null;
    });

    final ids = (await widget.interestPrefs.getInterestedIds()).toList();
    if (ids.isEmpty) {
      if (mounted) setState(() => _stage = _Stage.empty);
      return;
    }

    for (var attempt = 0; attempt < _maxRetries; attempt++) {
      final situationId = ids[_random.nextInt(ids.length)];
      try {
        final exercise = await widget.exerciseRepository.generate(situationId);
        if (mounted) {
          setState(() {
            _exercise = exercise;
            _stage = _Stage.front;
          });
        }
        return;
      } on ApiException catch (e) {
        if (e.statusCode == 404) {
          continue; // that situation had no exercisable content, try another
        }
        if (mounted) {
          setState(() {
            _errorMessage = e.message;
            _stage = _Stage.error;
          });
        }
        return;
      }
    }

    if (mounted) {
      setState(() {
        _errorMessage = 'No exercises available for your situations right now.';
        _stage = _Stage.error;
      });
    }
  }

  void _reveal() => setState(() => _stage = _Stage.revealed);

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
              ElevatedButton(
                onPressed: _startRound,
                child: const Text('Retry'),
              ),
            ],
          ),
        );
      case _Stage.error:
        return Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(_errorMessage ?? 'Something went wrong.', textAlign: TextAlign.center),
              const SizedBox(height: 16),
              ElevatedButton(onPressed: _startRound, child: const Text('Retry')),
            ],
          ),
        );
      case _Stage.front:
        return SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Flashcard(front: _exercise!.front),
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
                front: _exercise!.front,
                back: _exercise!.back,
                credits: _exercise!.credits,
              ),
              const SizedBox(height: 16),
              FsrsButtonRow(onAnswer: _startRound),
              const SizedBox(height: 16),
            ],
          ),
        );
    }
  }
}
