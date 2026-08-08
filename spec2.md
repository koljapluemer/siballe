Let's make this app a bit more useful.

Add a Profile tab, which we're actually not going to use for user/auth stuff yet.
For now, just add a text input (pw) to allow the user to add an open ai api key. This is only persisted on device (not on backend).

On the "Add" high level page, offer multiple options.
These all trigger different flows. 
For now, add two: "Add Sentence" and "Add Vocab".

Both of these are essentially the same form, this just preselects the KIND when they're saved to backend.

As first step of form, allow selecting language.
In this context, find some clean pattern that keeps iso3 codes as the source of truth in the backend, but allows users to see and select languages as the human-readable version on the frontend (e.g. vie/Vietnamese). This should NOT involve you hardcoding 12 languages you really like somewhere, but cleanly use libraries that provide ALL iso3 lists. This lang select should be a smart dropdown, i.e. a text field where the user writes which then suggests completions from dropdown. 

Next, situation select.
This should be another smart dropdown, but with some differences
- suggest situations that already exist for this language
- the user is not required to pick an existing situation; it is created if need be
- as a placeholder, put `"General $name_of_language"` in the textfield; and if the user leaves the field empty create this situation if needed and attach the data to it.

Then, a field to input the target language sentence or vocab (bit more space in case of sentences).
Then, a smart multi-form to add translations (for now these don't need a lang select, just hard-code them to `eng` in the background). 

All of these fields should also be smart dropdowns, suggesting relevant entries (since Nodes are unique-together for lang+kind+content).
This will lead to some merge challenges.
In the micro-app /home/brokkoli/GITHUB/sam-learns/src/apps/sentence-net (especially see form components and spec.md), I solved similar problems, please use this as inspiration.

Each of these fields is optional, but the user must *either* at least add one English translation or the target language word/sentence.

When form is confirmed, persist those sentences to backend.
But go one further:

If an API key provided, send it w/ the request and in backend generate additional structure.
Add missing translation/target (when only one of them is set). 
If a sentence was added, split it (only the target lang sentence, not the `eng` translation) into its component and correctly hook up these relationships as reciprocal EXAMPLE/PART_OF.
Then again add translations to these parts if needed.
If vocab was added, add example sentences and translations for that.

Again, in the sentence-net app, there are quite excellent LLM prompts for almost exactly this scenario; find and adapt them.
If a note is needed (e.g. word is meant in a specific sense of only in a specific context), put that in the `note` of the Rel connecting the vocab Node and its translation Node.
Link the directly added vocab/sentence to the situation with `relevance` 3, and the adjacent stuff (e.g. examples/parts) to it w/ relevance 2 (this has no effect yet, that's ok).
Do not add `credit`, this field is used to observe licences, not to spam.
add new state tuple entry `AUTO_GENERATED` where relevant and use where relevant (so AI gen stuff is clearly marked).

Make sure to add all the relevant stuff to django admin so I can see what has been going on generation-wise. 

