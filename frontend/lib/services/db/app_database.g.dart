// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'app_database.dart';

// ignore_for_file: type=lint
class $ExercisesTable extends Exercises
    with TableInfo<$ExercisesTable, ExerciseRow> {
  @override
  final GeneratedDatabase attachedDatabase;
  final String? _alias;
  $ExercisesTable(this.attachedDatabase, [this._alias]);
  static const VerificationMeta _idMeta = const VerificationMeta('id');
  @override
  late final GeneratedColumn<int> id = GeneratedColumn<int>(
    'id',
    aliasedName,
    false,
    type: DriftSqlType.int,
    requiredDuringInsert: false,
  );
  static const VerificationMeta _kindMeta = const VerificationMeta('kind');
  @override
  late final GeneratedColumn<String> kind = GeneratedColumn<String>(
    'kind',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _frontMeta = const VerificationMeta('front');
  @override
  late final GeneratedColumn<String> front = GeneratedColumn<String>(
    'front',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _backMeta = const VerificationMeta('back');
  @override
  late final GeneratedColumn<String> back = GeneratedColumn<String>(
    'back',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _creditsMeta = const VerificationMeta(
    'credits',
  );
  @override
  late final GeneratedColumn<String> credits = GeneratedColumn<String>(
    'credits',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _contentUpdatedAtMeta = const VerificationMeta(
    'contentUpdatedAt',
  );
  @override
  late final GeneratedColumn<DateTime> contentUpdatedAt =
      GeneratedColumn<DateTime>(
        'content_updated_at',
        aliasedName,
        false,
        type: DriftSqlType.dateTime,
        requiredDuringInsert: true,
      );
  @override
  List<GeneratedColumn> get $columns => [
    id,
    kind,
    front,
    back,
    credits,
    contentUpdatedAt,
  ];
  @override
  String get aliasedName => _alias ?? actualTableName;
  @override
  String get actualTableName => $name;
  static const String $name = 'exercises';
  @override
  VerificationContext validateIntegrity(
    Insertable<ExerciseRow> instance, {
    bool isInserting = false,
  }) {
    final context = VerificationContext();
    final data = instance.toColumns(true);
    if (data.containsKey('id')) {
      context.handle(_idMeta, id.isAcceptableOrUnknown(data['id']!, _idMeta));
    }
    if (data.containsKey('kind')) {
      context.handle(
        _kindMeta,
        kind.isAcceptableOrUnknown(data['kind']!, _kindMeta),
      );
    } else if (isInserting) {
      context.missing(_kindMeta);
    }
    if (data.containsKey('front')) {
      context.handle(
        _frontMeta,
        front.isAcceptableOrUnknown(data['front']!, _frontMeta),
      );
    } else if (isInserting) {
      context.missing(_frontMeta);
    }
    if (data.containsKey('back')) {
      context.handle(
        _backMeta,
        back.isAcceptableOrUnknown(data['back']!, _backMeta),
      );
    } else if (isInserting) {
      context.missing(_backMeta);
    }
    if (data.containsKey('credits')) {
      context.handle(
        _creditsMeta,
        credits.isAcceptableOrUnknown(data['credits']!, _creditsMeta),
      );
    } else if (isInserting) {
      context.missing(_creditsMeta);
    }
    if (data.containsKey('content_updated_at')) {
      context.handle(
        _contentUpdatedAtMeta,
        contentUpdatedAt.isAcceptableOrUnknown(
          data['content_updated_at']!,
          _contentUpdatedAtMeta,
        ),
      );
    } else if (isInserting) {
      context.missing(_contentUpdatedAtMeta);
    }
    return context;
  }

  @override
  Set<GeneratedColumn> get $primaryKey => {id};
  @override
  ExerciseRow map(Map<String, dynamic> data, {String? tablePrefix}) {
    final effectivePrefix = tablePrefix != null ? '$tablePrefix.' : '';
    return ExerciseRow(
      id: attachedDatabase.typeMapping.read(
        DriftSqlType.int,
        data['${effectivePrefix}id'],
      )!,
      kind: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}kind'],
      )!,
      front: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}front'],
      )!,
      back: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}back'],
      )!,
      credits: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}credits'],
      )!,
      contentUpdatedAt: attachedDatabase.typeMapping.read(
        DriftSqlType.dateTime,
        data['${effectivePrefix}content_updated_at'],
      )!,
    );
  }

  @override
  $ExercisesTable createAlias(String alias) {
    return $ExercisesTable(attachedDatabase, alias);
  }
}

class ExerciseRow extends DataClass implements Insertable<ExerciseRow> {
  final int id;
  final String kind;
  final String front;
  final String back;
  final String credits;
  final DateTime contentUpdatedAt;
  const ExerciseRow({
    required this.id,
    required this.kind,
    required this.front,
    required this.back,
    required this.credits,
    required this.contentUpdatedAt,
  });
  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    map['id'] = Variable<int>(id);
    map['kind'] = Variable<String>(kind);
    map['front'] = Variable<String>(front);
    map['back'] = Variable<String>(back);
    map['credits'] = Variable<String>(credits);
    map['content_updated_at'] = Variable<DateTime>(contentUpdatedAt);
    return map;
  }

  ExercisesCompanion toCompanion(bool nullToAbsent) {
    return ExercisesCompanion(
      id: Value(id),
      kind: Value(kind),
      front: Value(front),
      back: Value(back),
      credits: Value(credits),
      contentUpdatedAt: Value(contentUpdatedAt),
    );
  }

  factory ExerciseRow.fromJson(
    Map<String, dynamic> json, {
    ValueSerializer? serializer,
  }) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return ExerciseRow(
      id: serializer.fromJson<int>(json['id']),
      kind: serializer.fromJson<String>(json['kind']),
      front: serializer.fromJson<String>(json['front']),
      back: serializer.fromJson<String>(json['back']),
      credits: serializer.fromJson<String>(json['credits']),
      contentUpdatedAt: serializer.fromJson<DateTime>(json['contentUpdatedAt']),
    );
  }
  @override
  Map<String, dynamic> toJson({ValueSerializer? serializer}) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return <String, dynamic>{
      'id': serializer.toJson<int>(id),
      'kind': serializer.toJson<String>(kind),
      'front': serializer.toJson<String>(front),
      'back': serializer.toJson<String>(back),
      'credits': serializer.toJson<String>(credits),
      'contentUpdatedAt': serializer.toJson<DateTime>(contentUpdatedAt),
    };
  }

  ExerciseRow copyWith({
    int? id,
    String? kind,
    String? front,
    String? back,
    String? credits,
    DateTime? contentUpdatedAt,
  }) => ExerciseRow(
    id: id ?? this.id,
    kind: kind ?? this.kind,
    front: front ?? this.front,
    back: back ?? this.back,
    credits: credits ?? this.credits,
    contentUpdatedAt: contentUpdatedAt ?? this.contentUpdatedAt,
  );
  ExerciseRow copyWithCompanion(ExercisesCompanion data) {
    return ExerciseRow(
      id: data.id.present ? data.id.value : this.id,
      kind: data.kind.present ? data.kind.value : this.kind,
      front: data.front.present ? data.front.value : this.front,
      back: data.back.present ? data.back.value : this.back,
      credits: data.credits.present ? data.credits.value : this.credits,
      contentUpdatedAt: data.contentUpdatedAt.present
          ? data.contentUpdatedAt.value
          : this.contentUpdatedAt,
    );
  }

  @override
  String toString() {
    return (StringBuffer('ExerciseRow(')
          ..write('id: $id, ')
          ..write('kind: $kind, ')
          ..write('front: $front, ')
          ..write('back: $back, ')
          ..write('credits: $credits, ')
          ..write('contentUpdatedAt: $contentUpdatedAt')
          ..write(')'))
        .toString();
  }

  @override
  int get hashCode =>
      Object.hash(id, kind, front, back, credits, contentUpdatedAt);
  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      (other is ExerciseRow &&
          other.id == this.id &&
          other.kind == this.kind &&
          other.front == this.front &&
          other.back == this.back &&
          other.credits == this.credits &&
          other.contentUpdatedAt == this.contentUpdatedAt);
}

class ExercisesCompanion extends UpdateCompanion<ExerciseRow> {
  final Value<int> id;
  final Value<String> kind;
  final Value<String> front;
  final Value<String> back;
  final Value<String> credits;
  final Value<DateTime> contentUpdatedAt;
  const ExercisesCompanion({
    this.id = const Value.absent(),
    this.kind = const Value.absent(),
    this.front = const Value.absent(),
    this.back = const Value.absent(),
    this.credits = const Value.absent(),
    this.contentUpdatedAt = const Value.absent(),
  });
  ExercisesCompanion.insert({
    this.id = const Value.absent(),
    required String kind,
    required String front,
    required String back,
    required String credits,
    required DateTime contentUpdatedAt,
  }) : kind = Value(kind),
       front = Value(front),
       back = Value(back),
       credits = Value(credits),
       contentUpdatedAt = Value(contentUpdatedAt);
  static Insertable<ExerciseRow> custom({
    Expression<int>? id,
    Expression<String>? kind,
    Expression<String>? front,
    Expression<String>? back,
    Expression<String>? credits,
    Expression<DateTime>? contentUpdatedAt,
  }) {
    return RawValuesInsertable({
      if (id != null) 'id': id,
      if (kind != null) 'kind': kind,
      if (front != null) 'front': front,
      if (back != null) 'back': back,
      if (credits != null) 'credits': credits,
      if (contentUpdatedAt != null) 'content_updated_at': contentUpdatedAt,
    });
  }

  ExercisesCompanion copyWith({
    Value<int>? id,
    Value<String>? kind,
    Value<String>? front,
    Value<String>? back,
    Value<String>? credits,
    Value<DateTime>? contentUpdatedAt,
  }) {
    return ExercisesCompanion(
      id: id ?? this.id,
      kind: kind ?? this.kind,
      front: front ?? this.front,
      back: back ?? this.back,
      credits: credits ?? this.credits,
      contentUpdatedAt: contentUpdatedAt ?? this.contentUpdatedAt,
    );
  }

  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    if (id.present) {
      map['id'] = Variable<int>(id.value);
    }
    if (kind.present) {
      map['kind'] = Variable<String>(kind.value);
    }
    if (front.present) {
      map['front'] = Variable<String>(front.value);
    }
    if (back.present) {
      map['back'] = Variable<String>(back.value);
    }
    if (credits.present) {
      map['credits'] = Variable<String>(credits.value);
    }
    if (contentUpdatedAt.present) {
      map['content_updated_at'] = Variable<DateTime>(contentUpdatedAt.value);
    }
    return map;
  }

  @override
  String toString() {
    return (StringBuffer('ExercisesCompanion(')
          ..write('id: $id, ')
          ..write('kind: $kind, ')
          ..write('front: $front, ')
          ..write('back: $back, ')
          ..write('credits: $credits, ')
          ..write('contentUpdatedAt: $contentUpdatedAt')
          ..write(')'))
        .toString();
  }
}

class $ExerciseSituationsTable extends ExerciseSituations
    with TableInfo<$ExerciseSituationsTable, ExerciseSituationRow> {
  @override
  final GeneratedDatabase attachedDatabase;
  final String? _alias;
  $ExerciseSituationsTable(this.attachedDatabase, [this._alias]);
  static const VerificationMeta _exerciseIdMeta = const VerificationMeta(
    'exerciseId',
  );
  @override
  late final GeneratedColumn<int> exerciseId = GeneratedColumn<int>(
    'exercise_id',
    aliasedName,
    false,
    type: DriftSqlType.int,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _situationIdMeta = const VerificationMeta(
    'situationId',
  );
  @override
  late final GeneratedColumn<int> situationId = GeneratedColumn<int>(
    'situation_id',
    aliasedName,
    false,
    type: DriftSqlType.int,
    requiredDuringInsert: true,
  );
  @override
  List<GeneratedColumn> get $columns => [exerciseId, situationId];
  @override
  String get aliasedName => _alias ?? actualTableName;
  @override
  String get actualTableName => $name;
  static const String $name = 'exercise_situations';
  @override
  VerificationContext validateIntegrity(
    Insertable<ExerciseSituationRow> instance, {
    bool isInserting = false,
  }) {
    final context = VerificationContext();
    final data = instance.toColumns(true);
    if (data.containsKey('exercise_id')) {
      context.handle(
        _exerciseIdMeta,
        exerciseId.isAcceptableOrUnknown(data['exercise_id']!, _exerciseIdMeta),
      );
    } else if (isInserting) {
      context.missing(_exerciseIdMeta);
    }
    if (data.containsKey('situation_id')) {
      context.handle(
        _situationIdMeta,
        situationId.isAcceptableOrUnknown(
          data['situation_id']!,
          _situationIdMeta,
        ),
      );
    } else if (isInserting) {
      context.missing(_situationIdMeta);
    }
    return context;
  }

  @override
  Set<GeneratedColumn> get $primaryKey => {exerciseId, situationId};
  @override
  ExerciseSituationRow map(Map<String, dynamic> data, {String? tablePrefix}) {
    final effectivePrefix = tablePrefix != null ? '$tablePrefix.' : '';
    return ExerciseSituationRow(
      exerciseId: attachedDatabase.typeMapping.read(
        DriftSqlType.int,
        data['${effectivePrefix}exercise_id'],
      )!,
      situationId: attachedDatabase.typeMapping.read(
        DriftSqlType.int,
        data['${effectivePrefix}situation_id'],
      )!,
    );
  }

  @override
  $ExerciseSituationsTable createAlias(String alias) {
    return $ExerciseSituationsTable(attachedDatabase, alias);
  }
}

class ExerciseSituationRow extends DataClass
    implements Insertable<ExerciseSituationRow> {
  final int exerciseId;
  final int situationId;
  const ExerciseSituationRow({
    required this.exerciseId,
    required this.situationId,
  });
  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    map['exercise_id'] = Variable<int>(exerciseId);
    map['situation_id'] = Variable<int>(situationId);
    return map;
  }

  ExerciseSituationsCompanion toCompanion(bool nullToAbsent) {
    return ExerciseSituationsCompanion(
      exerciseId: Value(exerciseId),
      situationId: Value(situationId),
    );
  }

  factory ExerciseSituationRow.fromJson(
    Map<String, dynamic> json, {
    ValueSerializer? serializer,
  }) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return ExerciseSituationRow(
      exerciseId: serializer.fromJson<int>(json['exerciseId']),
      situationId: serializer.fromJson<int>(json['situationId']),
    );
  }
  @override
  Map<String, dynamic> toJson({ValueSerializer? serializer}) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return <String, dynamic>{
      'exerciseId': serializer.toJson<int>(exerciseId),
      'situationId': serializer.toJson<int>(situationId),
    };
  }

  ExerciseSituationRow copyWith({int? exerciseId, int? situationId}) =>
      ExerciseSituationRow(
        exerciseId: exerciseId ?? this.exerciseId,
        situationId: situationId ?? this.situationId,
      );
  ExerciseSituationRow copyWithCompanion(ExerciseSituationsCompanion data) {
    return ExerciseSituationRow(
      exerciseId: data.exerciseId.present
          ? data.exerciseId.value
          : this.exerciseId,
      situationId: data.situationId.present
          ? data.situationId.value
          : this.situationId,
    );
  }

  @override
  String toString() {
    return (StringBuffer('ExerciseSituationRow(')
          ..write('exerciseId: $exerciseId, ')
          ..write('situationId: $situationId')
          ..write(')'))
        .toString();
  }

  @override
  int get hashCode => Object.hash(exerciseId, situationId);
  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      (other is ExerciseSituationRow &&
          other.exerciseId == this.exerciseId &&
          other.situationId == this.situationId);
}

class ExerciseSituationsCompanion
    extends UpdateCompanion<ExerciseSituationRow> {
  final Value<int> exerciseId;
  final Value<int> situationId;
  final Value<int> rowid;
  const ExerciseSituationsCompanion({
    this.exerciseId = const Value.absent(),
    this.situationId = const Value.absent(),
    this.rowid = const Value.absent(),
  });
  ExerciseSituationsCompanion.insert({
    required int exerciseId,
    required int situationId,
    this.rowid = const Value.absent(),
  }) : exerciseId = Value(exerciseId),
       situationId = Value(situationId);
  static Insertable<ExerciseSituationRow> custom({
    Expression<int>? exerciseId,
    Expression<int>? situationId,
    Expression<int>? rowid,
  }) {
    return RawValuesInsertable({
      if (exerciseId != null) 'exercise_id': exerciseId,
      if (situationId != null) 'situation_id': situationId,
      if (rowid != null) 'rowid': rowid,
    });
  }

  ExerciseSituationsCompanion copyWith({
    Value<int>? exerciseId,
    Value<int>? situationId,
    Value<int>? rowid,
  }) {
    return ExerciseSituationsCompanion(
      exerciseId: exerciseId ?? this.exerciseId,
      situationId: situationId ?? this.situationId,
      rowid: rowid ?? this.rowid,
    );
  }

  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    if (exerciseId.present) {
      map['exercise_id'] = Variable<int>(exerciseId.value);
    }
    if (situationId.present) {
      map['situation_id'] = Variable<int>(situationId.value);
    }
    if (rowid.present) {
      map['rowid'] = Variable<int>(rowid.value);
    }
    return map;
  }

  @override
  String toString() {
    return (StringBuffer('ExerciseSituationsCompanion(')
          ..write('exerciseId: $exerciseId, ')
          ..write('situationId: $situationId, ')
          ..write('rowid: $rowid')
          ..write(')'))
        .toString();
  }
}

class $ReviewCardsTable extends ReviewCards
    with TableInfo<$ReviewCardsTable, ReviewCardRow> {
  @override
  final GeneratedDatabase attachedDatabase;
  final String? _alias;
  $ReviewCardsTable(this.attachedDatabase, [this._alias]);
  static const VerificationMeta _exerciseIdMeta = const VerificationMeta(
    'exerciseId',
  );
  @override
  late final GeneratedColumn<int> exerciseId = GeneratedColumn<int>(
    'exercise_id',
    aliasedName,
    false,
    type: DriftSqlType.int,
    requiredDuringInsert: false,
  );
  static const VerificationMeta _cardJsonMeta = const VerificationMeta(
    'cardJson',
  );
  @override
  late final GeneratedColumn<String> cardJson = GeneratedColumn<String>(
    'card_json',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _dueMeta = const VerificationMeta('due');
  @override
  late final GeneratedColumn<DateTime> due = GeneratedColumn<DateTime>(
    'due',
    aliasedName,
    false,
    type: DriftSqlType.dateTime,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _updatedAtMeta = const VerificationMeta(
    'updatedAt',
  );
  @override
  late final GeneratedColumn<DateTime> updatedAt = GeneratedColumn<DateTime>(
    'updated_at',
    aliasedName,
    false,
    type: DriftSqlType.dateTime,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _dirtyMeta = const VerificationMeta('dirty');
  @override
  late final GeneratedColumn<bool> dirty = GeneratedColumn<bool>(
    'dirty',
    aliasedName,
    false,
    type: DriftSqlType.bool,
    requiredDuringInsert: false,
    defaultConstraints: GeneratedColumn.constraintIsAlways(
      'CHECK ("dirty" IN (0, 1))',
    ),
    defaultValue: const Constant(true),
  );
  @override
  List<GeneratedColumn> get $columns => [
    exerciseId,
    cardJson,
    due,
    updatedAt,
    dirty,
  ];
  @override
  String get aliasedName => _alias ?? actualTableName;
  @override
  String get actualTableName => $name;
  static const String $name = 'review_cards';
  @override
  VerificationContext validateIntegrity(
    Insertable<ReviewCardRow> instance, {
    bool isInserting = false,
  }) {
    final context = VerificationContext();
    final data = instance.toColumns(true);
    if (data.containsKey('exercise_id')) {
      context.handle(
        _exerciseIdMeta,
        exerciseId.isAcceptableOrUnknown(data['exercise_id']!, _exerciseIdMeta),
      );
    }
    if (data.containsKey('card_json')) {
      context.handle(
        _cardJsonMeta,
        cardJson.isAcceptableOrUnknown(data['card_json']!, _cardJsonMeta),
      );
    } else if (isInserting) {
      context.missing(_cardJsonMeta);
    }
    if (data.containsKey('due')) {
      context.handle(
        _dueMeta,
        due.isAcceptableOrUnknown(data['due']!, _dueMeta),
      );
    } else if (isInserting) {
      context.missing(_dueMeta);
    }
    if (data.containsKey('updated_at')) {
      context.handle(
        _updatedAtMeta,
        updatedAt.isAcceptableOrUnknown(data['updated_at']!, _updatedAtMeta),
      );
    } else if (isInserting) {
      context.missing(_updatedAtMeta);
    }
    if (data.containsKey('dirty')) {
      context.handle(
        _dirtyMeta,
        dirty.isAcceptableOrUnknown(data['dirty']!, _dirtyMeta),
      );
    }
    return context;
  }

  @override
  Set<GeneratedColumn> get $primaryKey => {exerciseId};
  @override
  ReviewCardRow map(Map<String, dynamic> data, {String? tablePrefix}) {
    final effectivePrefix = tablePrefix != null ? '$tablePrefix.' : '';
    return ReviewCardRow(
      exerciseId: attachedDatabase.typeMapping.read(
        DriftSqlType.int,
        data['${effectivePrefix}exercise_id'],
      )!,
      cardJson: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}card_json'],
      )!,
      due: attachedDatabase.typeMapping.read(
        DriftSqlType.dateTime,
        data['${effectivePrefix}due'],
      )!,
      updatedAt: attachedDatabase.typeMapping.read(
        DriftSqlType.dateTime,
        data['${effectivePrefix}updated_at'],
      )!,
      dirty: attachedDatabase.typeMapping.read(
        DriftSqlType.bool,
        data['${effectivePrefix}dirty'],
      )!,
    );
  }

  @override
  $ReviewCardsTable createAlias(String alias) {
    return $ReviewCardsTable(attachedDatabase, alias);
  }
}

class ReviewCardRow extends DataClass implements Insertable<ReviewCardRow> {
  final int exerciseId;
  final String cardJson;
  final DateTime due;
  final DateTime updatedAt;
  final bool dirty;
  const ReviewCardRow({
    required this.exerciseId,
    required this.cardJson,
    required this.due,
    required this.updatedAt,
    required this.dirty,
  });
  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    map['exercise_id'] = Variable<int>(exerciseId);
    map['card_json'] = Variable<String>(cardJson);
    map['due'] = Variable<DateTime>(due);
    map['updated_at'] = Variable<DateTime>(updatedAt);
    map['dirty'] = Variable<bool>(dirty);
    return map;
  }

  ReviewCardsCompanion toCompanion(bool nullToAbsent) {
    return ReviewCardsCompanion(
      exerciseId: Value(exerciseId),
      cardJson: Value(cardJson),
      due: Value(due),
      updatedAt: Value(updatedAt),
      dirty: Value(dirty),
    );
  }

  factory ReviewCardRow.fromJson(
    Map<String, dynamic> json, {
    ValueSerializer? serializer,
  }) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return ReviewCardRow(
      exerciseId: serializer.fromJson<int>(json['exerciseId']),
      cardJson: serializer.fromJson<String>(json['cardJson']),
      due: serializer.fromJson<DateTime>(json['due']),
      updatedAt: serializer.fromJson<DateTime>(json['updatedAt']),
      dirty: serializer.fromJson<bool>(json['dirty']),
    );
  }
  @override
  Map<String, dynamic> toJson({ValueSerializer? serializer}) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return <String, dynamic>{
      'exerciseId': serializer.toJson<int>(exerciseId),
      'cardJson': serializer.toJson<String>(cardJson),
      'due': serializer.toJson<DateTime>(due),
      'updatedAt': serializer.toJson<DateTime>(updatedAt),
      'dirty': serializer.toJson<bool>(dirty),
    };
  }

  ReviewCardRow copyWith({
    int? exerciseId,
    String? cardJson,
    DateTime? due,
    DateTime? updatedAt,
    bool? dirty,
  }) => ReviewCardRow(
    exerciseId: exerciseId ?? this.exerciseId,
    cardJson: cardJson ?? this.cardJson,
    due: due ?? this.due,
    updatedAt: updatedAt ?? this.updatedAt,
    dirty: dirty ?? this.dirty,
  );
  ReviewCardRow copyWithCompanion(ReviewCardsCompanion data) {
    return ReviewCardRow(
      exerciseId: data.exerciseId.present
          ? data.exerciseId.value
          : this.exerciseId,
      cardJson: data.cardJson.present ? data.cardJson.value : this.cardJson,
      due: data.due.present ? data.due.value : this.due,
      updatedAt: data.updatedAt.present ? data.updatedAt.value : this.updatedAt,
      dirty: data.dirty.present ? data.dirty.value : this.dirty,
    );
  }

  @override
  String toString() {
    return (StringBuffer('ReviewCardRow(')
          ..write('exerciseId: $exerciseId, ')
          ..write('cardJson: $cardJson, ')
          ..write('due: $due, ')
          ..write('updatedAt: $updatedAt, ')
          ..write('dirty: $dirty')
          ..write(')'))
        .toString();
  }

  @override
  int get hashCode => Object.hash(exerciseId, cardJson, due, updatedAt, dirty);
  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      (other is ReviewCardRow &&
          other.exerciseId == this.exerciseId &&
          other.cardJson == this.cardJson &&
          other.due == this.due &&
          other.updatedAt == this.updatedAt &&
          other.dirty == this.dirty);
}

class ReviewCardsCompanion extends UpdateCompanion<ReviewCardRow> {
  final Value<int> exerciseId;
  final Value<String> cardJson;
  final Value<DateTime> due;
  final Value<DateTime> updatedAt;
  final Value<bool> dirty;
  const ReviewCardsCompanion({
    this.exerciseId = const Value.absent(),
    this.cardJson = const Value.absent(),
    this.due = const Value.absent(),
    this.updatedAt = const Value.absent(),
    this.dirty = const Value.absent(),
  });
  ReviewCardsCompanion.insert({
    this.exerciseId = const Value.absent(),
    required String cardJson,
    required DateTime due,
    required DateTime updatedAt,
    this.dirty = const Value.absent(),
  }) : cardJson = Value(cardJson),
       due = Value(due),
       updatedAt = Value(updatedAt);
  static Insertable<ReviewCardRow> custom({
    Expression<int>? exerciseId,
    Expression<String>? cardJson,
    Expression<DateTime>? due,
    Expression<DateTime>? updatedAt,
    Expression<bool>? dirty,
  }) {
    return RawValuesInsertable({
      if (exerciseId != null) 'exercise_id': exerciseId,
      if (cardJson != null) 'card_json': cardJson,
      if (due != null) 'due': due,
      if (updatedAt != null) 'updated_at': updatedAt,
      if (dirty != null) 'dirty': dirty,
    });
  }

  ReviewCardsCompanion copyWith({
    Value<int>? exerciseId,
    Value<String>? cardJson,
    Value<DateTime>? due,
    Value<DateTime>? updatedAt,
    Value<bool>? dirty,
  }) {
    return ReviewCardsCompanion(
      exerciseId: exerciseId ?? this.exerciseId,
      cardJson: cardJson ?? this.cardJson,
      due: due ?? this.due,
      updatedAt: updatedAt ?? this.updatedAt,
      dirty: dirty ?? this.dirty,
    );
  }

  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    if (exerciseId.present) {
      map['exercise_id'] = Variable<int>(exerciseId.value);
    }
    if (cardJson.present) {
      map['card_json'] = Variable<String>(cardJson.value);
    }
    if (due.present) {
      map['due'] = Variable<DateTime>(due.value);
    }
    if (updatedAt.present) {
      map['updated_at'] = Variable<DateTime>(updatedAt.value);
    }
    if (dirty.present) {
      map['dirty'] = Variable<bool>(dirty.value);
    }
    return map;
  }

  @override
  String toString() {
    return (StringBuffer('ReviewCardsCompanion(')
          ..write('exerciseId: $exerciseId, ')
          ..write('cardJson: $cardJson, ')
          ..write('due: $due, ')
          ..write('updatedAt: $updatedAt, ')
          ..write('dirty: $dirty')
          ..write(')'))
        .toString();
  }
}

abstract class _$AppDatabase extends GeneratedDatabase {
  _$AppDatabase(QueryExecutor e) : super(e);
  $AppDatabaseManager get managers => $AppDatabaseManager(this);
  late final $ExercisesTable exercises = $ExercisesTable(this);
  late final $ExerciseSituationsTable exerciseSituations =
      $ExerciseSituationsTable(this);
  late final $ReviewCardsTable reviewCards = $ReviewCardsTable(this);
  @override
  Iterable<TableInfo<Table, Object?>> get allTables =>
      allSchemaEntities.whereType<TableInfo<Table, Object?>>();
  @override
  List<DatabaseSchemaEntity> get allSchemaEntities => [
    exercises,
    exerciseSituations,
    reviewCards,
  ];
}

typedef $$ExercisesTableCreateCompanionBuilder =
    ExercisesCompanion Function({
      Value<int> id,
      required String kind,
      required String front,
      required String back,
      required String credits,
      required DateTime contentUpdatedAt,
    });
typedef $$ExercisesTableUpdateCompanionBuilder =
    ExercisesCompanion Function({
      Value<int> id,
      Value<String> kind,
      Value<String> front,
      Value<String> back,
      Value<String> credits,
      Value<DateTime> contentUpdatedAt,
    });

class $$ExercisesTableFilterComposer
    extends Composer<_$AppDatabase, $ExercisesTable> {
  $$ExercisesTableFilterComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnFilters<int> get id => $composableBuilder(
    column: $table.id,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get kind => $composableBuilder(
    column: $table.kind,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get front => $composableBuilder(
    column: $table.front,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get back => $composableBuilder(
    column: $table.back,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get credits => $composableBuilder(
    column: $table.credits,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<DateTime> get contentUpdatedAt => $composableBuilder(
    column: $table.contentUpdatedAt,
    builder: (column) => ColumnFilters(column),
  );
}

class $$ExercisesTableOrderingComposer
    extends Composer<_$AppDatabase, $ExercisesTable> {
  $$ExercisesTableOrderingComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnOrderings<int> get id => $composableBuilder(
    column: $table.id,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get kind => $composableBuilder(
    column: $table.kind,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get front => $composableBuilder(
    column: $table.front,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get back => $composableBuilder(
    column: $table.back,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get credits => $composableBuilder(
    column: $table.credits,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<DateTime> get contentUpdatedAt => $composableBuilder(
    column: $table.contentUpdatedAt,
    builder: (column) => ColumnOrderings(column),
  );
}

class $$ExercisesTableAnnotationComposer
    extends Composer<_$AppDatabase, $ExercisesTable> {
  $$ExercisesTableAnnotationComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  GeneratedColumn<int> get id =>
      $composableBuilder(column: $table.id, builder: (column) => column);

  GeneratedColumn<String> get kind =>
      $composableBuilder(column: $table.kind, builder: (column) => column);

  GeneratedColumn<String> get front =>
      $composableBuilder(column: $table.front, builder: (column) => column);

  GeneratedColumn<String> get back =>
      $composableBuilder(column: $table.back, builder: (column) => column);

  GeneratedColumn<String> get credits =>
      $composableBuilder(column: $table.credits, builder: (column) => column);

  GeneratedColumn<DateTime> get contentUpdatedAt => $composableBuilder(
    column: $table.contentUpdatedAt,
    builder: (column) => column,
  );
}

class $$ExercisesTableTableManager
    extends
        RootTableManager<
          _$AppDatabase,
          $ExercisesTable,
          ExerciseRow,
          $$ExercisesTableFilterComposer,
          $$ExercisesTableOrderingComposer,
          $$ExercisesTableAnnotationComposer,
          $$ExercisesTableCreateCompanionBuilder,
          $$ExercisesTableUpdateCompanionBuilder,
          (
            ExerciseRow,
            BaseReferences<_$AppDatabase, $ExercisesTable, ExerciseRow>,
          ),
          ExerciseRow,
          PrefetchHooks Function()
        > {
  $$ExercisesTableTableManager(_$AppDatabase db, $ExercisesTable table)
    : super(
        TableManagerState(
          db: db,
          table: table,
          createFilteringComposer: () =>
              $$ExercisesTableFilterComposer($db: db, $table: table),
          createOrderingComposer: () =>
              $$ExercisesTableOrderingComposer($db: db, $table: table),
          createComputedFieldComposer: () =>
              $$ExercisesTableAnnotationComposer($db: db, $table: table),
          updateCompanionCallback:
              ({
                Value<int> id = const Value.absent(),
                Value<String> kind = const Value.absent(),
                Value<String> front = const Value.absent(),
                Value<String> back = const Value.absent(),
                Value<String> credits = const Value.absent(),
                Value<DateTime> contentUpdatedAt = const Value.absent(),
              }) => ExercisesCompanion(
                id: id,
                kind: kind,
                front: front,
                back: back,
                credits: credits,
                contentUpdatedAt: contentUpdatedAt,
              ),
          createCompanionCallback:
              ({
                Value<int> id = const Value.absent(),
                required String kind,
                required String front,
                required String back,
                required String credits,
                required DateTime contentUpdatedAt,
              }) => ExercisesCompanion.insert(
                id: id,
                kind: kind,
                front: front,
                back: back,
                credits: credits,
                contentUpdatedAt: contentUpdatedAt,
              ),
          withReferenceMapper: (p0) => p0
              .map((e) => (e.readTable(table), BaseReferences(db, table, e)))
              .toList(),
          prefetchHooksCallback: null,
        ),
      );
}

typedef $$ExercisesTableProcessedTableManager =
    ProcessedTableManager<
      _$AppDatabase,
      $ExercisesTable,
      ExerciseRow,
      $$ExercisesTableFilterComposer,
      $$ExercisesTableOrderingComposer,
      $$ExercisesTableAnnotationComposer,
      $$ExercisesTableCreateCompanionBuilder,
      $$ExercisesTableUpdateCompanionBuilder,
      (
        ExerciseRow,
        BaseReferences<_$AppDatabase, $ExercisesTable, ExerciseRow>,
      ),
      ExerciseRow,
      PrefetchHooks Function()
    >;
typedef $$ExerciseSituationsTableCreateCompanionBuilder =
    ExerciseSituationsCompanion Function({
      required int exerciseId,
      required int situationId,
      Value<int> rowid,
    });
typedef $$ExerciseSituationsTableUpdateCompanionBuilder =
    ExerciseSituationsCompanion Function({
      Value<int> exerciseId,
      Value<int> situationId,
      Value<int> rowid,
    });

class $$ExerciseSituationsTableFilterComposer
    extends Composer<_$AppDatabase, $ExerciseSituationsTable> {
  $$ExerciseSituationsTableFilterComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnFilters<int> get exerciseId => $composableBuilder(
    column: $table.exerciseId,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<int> get situationId => $composableBuilder(
    column: $table.situationId,
    builder: (column) => ColumnFilters(column),
  );
}

class $$ExerciseSituationsTableOrderingComposer
    extends Composer<_$AppDatabase, $ExerciseSituationsTable> {
  $$ExerciseSituationsTableOrderingComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnOrderings<int> get exerciseId => $composableBuilder(
    column: $table.exerciseId,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<int> get situationId => $composableBuilder(
    column: $table.situationId,
    builder: (column) => ColumnOrderings(column),
  );
}

class $$ExerciseSituationsTableAnnotationComposer
    extends Composer<_$AppDatabase, $ExerciseSituationsTable> {
  $$ExerciseSituationsTableAnnotationComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  GeneratedColumn<int> get exerciseId => $composableBuilder(
    column: $table.exerciseId,
    builder: (column) => column,
  );

  GeneratedColumn<int> get situationId => $composableBuilder(
    column: $table.situationId,
    builder: (column) => column,
  );
}

class $$ExerciseSituationsTableTableManager
    extends
        RootTableManager<
          _$AppDatabase,
          $ExerciseSituationsTable,
          ExerciseSituationRow,
          $$ExerciseSituationsTableFilterComposer,
          $$ExerciseSituationsTableOrderingComposer,
          $$ExerciseSituationsTableAnnotationComposer,
          $$ExerciseSituationsTableCreateCompanionBuilder,
          $$ExerciseSituationsTableUpdateCompanionBuilder,
          (
            ExerciseSituationRow,
            BaseReferences<
              _$AppDatabase,
              $ExerciseSituationsTable,
              ExerciseSituationRow
            >,
          ),
          ExerciseSituationRow,
          PrefetchHooks Function()
        > {
  $$ExerciseSituationsTableTableManager(
    _$AppDatabase db,
    $ExerciseSituationsTable table,
  ) : super(
        TableManagerState(
          db: db,
          table: table,
          createFilteringComposer: () =>
              $$ExerciseSituationsTableFilterComposer($db: db, $table: table),
          createOrderingComposer: () =>
              $$ExerciseSituationsTableOrderingComposer($db: db, $table: table),
          createComputedFieldComposer: () =>
              $$ExerciseSituationsTableAnnotationComposer(
                $db: db,
                $table: table,
              ),
          updateCompanionCallback:
              ({
                Value<int> exerciseId = const Value.absent(),
                Value<int> situationId = const Value.absent(),
                Value<int> rowid = const Value.absent(),
              }) => ExerciseSituationsCompanion(
                exerciseId: exerciseId,
                situationId: situationId,
                rowid: rowid,
              ),
          createCompanionCallback:
              ({
                required int exerciseId,
                required int situationId,
                Value<int> rowid = const Value.absent(),
              }) => ExerciseSituationsCompanion.insert(
                exerciseId: exerciseId,
                situationId: situationId,
                rowid: rowid,
              ),
          withReferenceMapper: (p0) => p0
              .map((e) => (e.readTable(table), BaseReferences(db, table, e)))
              .toList(),
          prefetchHooksCallback: null,
        ),
      );
}

typedef $$ExerciseSituationsTableProcessedTableManager =
    ProcessedTableManager<
      _$AppDatabase,
      $ExerciseSituationsTable,
      ExerciseSituationRow,
      $$ExerciseSituationsTableFilterComposer,
      $$ExerciseSituationsTableOrderingComposer,
      $$ExerciseSituationsTableAnnotationComposer,
      $$ExerciseSituationsTableCreateCompanionBuilder,
      $$ExerciseSituationsTableUpdateCompanionBuilder,
      (
        ExerciseSituationRow,
        BaseReferences<
          _$AppDatabase,
          $ExerciseSituationsTable,
          ExerciseSituationRow
        >,
      ),
      ExerciseSituationRow,
      PrefetchHooks Function()
    >;
typedef $$ReviewCardsTableCreateCompanionBuilder =
    ReviewCardsCompanion Function({
      Value<int> exerciseId,
      required String cardJson,
      required DateTime due,
      required DateTime updatedAt,
      Value<bool> dirty,
    });
typedef $$ReviewCardsTableUpdateCompanionBuilder =
    ReviewCardsCompanion Function({
      Value<int> exerciseId,
      Value<String> cardJson,
      Value<DateTime> due,
      Value<DateTime> updatedAt,
      Value<bool> dirty,
    });

class $$ReviewCardsTableFilterComposer
    extends Composer<_$AppDatabase, $ReviewCardsTable> {
  $$ReviewCardsTableFilterComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnFilters<int> get exerciseId => $composableBuilder(
    column: $table.exerciseId,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get cardJson => $composableBuilder(
    column: $table.cardJson,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<DateTime> get due => $composableBuilder(
    column: $table.due,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<DateTime> get updatedAt => $composableBuilder(
    column: $table.updatedAt,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<bool> get dirty => $composableBuilder(
    column: $table.dirty,
    builder: (column) => ColumnFilters(column),
  );
}

class $$ReviewCardsTableOrderingComposer
    extends Composer<_$AppDatabase, $ReviewCardsTable> {
  $$ReviewCardsTableOrderingComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnOrderings<int> get exerciseId => $composableBuilder(
    column: $table.exerciseId,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get cardJson => $composableBuilder(
    column: $table.cardJson,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<DateTime> get due => $composableBuilder(
    column: $table.due,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<DateTime> get updatedAt => $composableBuilder(
    column: $table.updatedAt,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<bool> get dirty => $composableBuilder(
    column: $table.dirty,
    builder: (column) => ColumnOrderings(column),
  );
}

class $$ReviewCardsTableAnnotationComposer
    extends Composer<_$AppDatabase, $ReviewCardsTable> {
  $$ReviewCardsTableAnnotationComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  GeneratedColumn<int> get exerciseId => $composableBuilder(
    column: $table.exerciseId,
    builder: (column) => column,
  );

  GeneratedColumn<String> get cardJson =>
      $composableBuilder(column: $table.cardJson, builder: (column) => column);

  GeneratedColumn<DateTime> get due =>
      $composableBuilder(column: $table.due, builder: (column) => column);

  GeneratedColumn<DateTime> get updatedAt =>
      $composableBuilder(column: $table.updatedAt, builder: (column) => column);

  GeneratedColumn<bool> get dirty =>
      $composableBuilder(column: $table.dirty, builder: (column) => column);
}

class $$ReviewCardsTableTableManager
    extends
        RootTableManager<
          _$AppDatabase,
          $ReviewCardsTable,
          ReviewCardRow,
          $$ReviewCardsTableFilterComposer,
          $$ReviewCardsTableOrderingComposer,
          $$ReviewCardsTableAnnotationComposer,
          $$ReviewCardsTableCreateCompanionBuilder,
          $$ReviewCardsTableUpdateCompanionBuilder,
          (
            ReviewCardRow,
            BaseReferences<_$AppDatabase, $ReviewCardsTable, ReviewCardRow>,
          ),
          ReviewCardRow,
          PrefetchHooks Function()
        > {
  $$ReviewCardsTableTableManager(_$AppDatabase db, $ReviewCardsTable table)
    : super(
        TableManagerState(
          db: db,
          table: table,
          createFilteringComposer: () =>
              $$ReviewCardsTableFilterComposer($db: db, $table: table),
          createOrderingComposer: () =>
              $$ReviewCardsTableOrderingComposer($db: db, $table: table),
          createComputedFieldComposer: () =>
              $$ReviewCardsTableAnnotationComposer($db: db, $table: table),
          updateCompanionCallback:
              ({
                Value<int> exerciseId = const Value.absent(),
                Value<String> cardJson = const Value.absent(),
                Value<DateTime> due = const Value.absent(),
                Value<DateTime> updatedAt = const Value.absent(),
                Value<bool> dirty = const Value.absent(),
              }) => ReviewCardsCompanion(
                exerciseId: exerciseId,
                cardJson: cardJson,
                due: due,
                updatedAt: updatedAt,
                dirty: dirty,
              ),
          createCompanionCallback:
              ({
                Value<int> exerciseId = const Value.absent(),
                required String cardJson,
                required DateTime due,
                required DateTime updatedAt,
                Value<bool> dirty = const Value.absent(),
              }) => ReviewCardsCompanion.insert(
                exerciseId: exerciseId,
                cardJson: cardJson,
                due: due,
                updatedAt: updatedAt,
                dirty: dirty,
              ),
          withReferenceMapper: (p0) => p0
              .map((e) => (e.readTable(table), BaseReferences(db, table, e)))
              .toList(),
          prefetchHooksCallback: null,
        ),
      );
}

typedef $$ReviewCardsTableProcessedTableManager =
    ProcessedTableManager<
      _$AppDatabase,
      $ReviewCardsTable,
      ReviewCardRow,
      $$ReviewCardsTableFilterComposer,
      $$ReviewCardsTableOrderingComposer,
      $$ReviewCardsTableAnnotationComposer,
      $$ReviewCardsTableCreateCompanionBuilder,
      $$ReviewCardsTableUpdateCompanionBuilder,
      (
        ReviewCardRow,
        BaseReferences<_$AppDatabase, $ReviewCardsTable, ReviewCardRow>,
      ),
      ReviewCardRow,
      PrefetchHooks Function()
    >;

class $AppDatabaseManager {
  final _$AppDatabase _db;
  $AppDatabaseManager(this._db);
  $$ExercisesTableTableManager get exercises =>
      $$ExercisesTableTableManager(_db, _db.exercises);
  $$ExerciseSituationsTableTableManager get exerciseSituations =>
      $$ExerciseSituationsTableTableManager(_db, _db.exerciseSituations);
  $$ReviewCardsTableTableManager get reviewCards =>
      $$ReviewCardsTableTableManager(_db, _db.reviewCards);
}
