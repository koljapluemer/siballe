Core stack: Django REST backend w/ auth, frontend Flutter (deployed to web and android, at a later point maybe iOS)

Core idea: A language learning app, for now mostly based on interconnected sentences and words, relating to situations (such as "buying something in the bakery")

## Flutter

Use simple standard patterns.
Have a bottom bar with (icon) buttons that navigate to main pages.

For now, the following pages:
- Learn (Play Button)
- Add (for now stub/leave empty)
- Situations 

### Pages

#### Situations

Simply fetch `situations/` and display.
Each situation should have a checkbox where the user can select whether they are interested in learning the language relating to this situation, or not. Persist this choice in frontend.

#### Learn

For now, pick a random situation from the ones the user is trying to learn, and call the exercise gen endpoint, and render that exercise in a standard flashcard flow (first show `front` in a card format and a button "Reveal", then show `front`, a divider line, and `back` on the card, standard fsrs buttons "Wrong", "Hard", "Correct", "Easy" (they all just load next random exercise for now) and a box with the credits in tiny font below that.

For this MVP, no learning data is actually persisted.

## Django 

Should be a simple single-django-app setup, using uv for management.
Should use a folder structure (e.g. views/ and models/ instead views.py and models.py). 
Standard Django patterns whenever possible (but not tutorial shit, this WILL BE growing).
Make ready for ubuntu VPS deploy (staticfiles, postgres, ...) and so on so we don't have to change setup later.
I mentioned that this app should have auth; this isn't actually relevant for functionality now but usually requires some hard-to-change setup, so I rather would get this done now.

Provides the learning data.
Overtime, the app's value will be that we map relationships between sentences, words/vocab, materials etc., and can thus granually provide relevant and related learning exercises. Thus, we will model a fairly abstract graph-style concept:

Node # may be vocab, sentence, video link...
- kind (feeds from a hardcoded list of node types, for now: VOCAB, SENTENCE)
- language (can be any iso3 code, get a library for this)
- content:text
- credit?:text
- state (hardcoded list again, for now: TRUSTED, `NEEDS_CHECKING`)

# kind+language+content should be unique-together

Rel # relationship between two nodes
- sender: node
- receiver: node
- label (hardcoded list, for now: EXAMPLE, `PART_OF`, `TRANSLATION`)
- note?: text
- credit?: text
- state (hardcoded list again, for now: TRUSTED, `NEEDS_CHECKING`) (this is a different list from the node states!)

Situation 
- language: iso3 code
- description: english text (unique)

SituationRelation
- situation
- node
- relevance (int from 0 to 5 inclusive)

### API

#### /situations

Return the available situations, grouped by languages

#### generate exercise for situation

Requires a situation id. 
Gets that situation, and then via SituationRelation gets a random relevant Node (is connected, and relevance is >=2).

For now, we generate just the following types of exercises:
- If node is VOCAB, return a "FlashcardVocab" exercise:

- kind: `FlashcardVocab`
- front: "What does this mean? /n/n ## $node.content"
- back: pick up to 3 random VOCAB nodes that are connected via a TRANSLATION label Rel, and have language `eng` (for now, hardcoding this). Also pick (up to) 2 random nodes that are SENTENCE, connected via label Rel as EXAMPLE, have the same language, and include their translations (`eng` language SENTENCE node connected as TRANSLATION) — do not return sentences that do not have such a translation. Render the translations in randomized order as "### $translation \n"; include the relationship note (if exists) after the line as "*$note* \n\n". After that, have a simple section with the example sentence, always first the target language sentence in bold, then linebreak, translation, double linebreak, next
- credits: concat all credits (relationships+nodes) with ";" as simple inline-markdown rendered string

- If node is SENTENCE, return a "FlashcardSentence" exercise: 

Very similar to the structure above. On the front, show just the sentence (format "What does this mean? /n/n #### $node.content), then on the back the translation, and a list of parts (=PART_OF) in the same format as the example sentences described above

### Bootstrap Data

Construct a very simple JSON with some kickstart data for `fra`, situation "Smalltalk in French", with a couple sentences, and their parts, and example for those parts. Just for testing. Add an admin script to load this data in. 

### Doc

- Add a brief README on how to run and HIGHEST LEVEL!! architecture
- Add a justfile with a `just dev` command
