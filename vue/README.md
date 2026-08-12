## Essential Tech Stack

- vite+vue
- tailwind + Daisy UI. Actually use daisy components. Avoid manual CSS when possible.
- lucide icons (via the vue package)
- vue router
- dexie as local source of truth for data 

## Architecture

layered architecture w/ the following high level folders:

- `db`: Holding dexie infrastructure and DB types. Necessary evil. Should be as small as possible
- `dumb`: collection of simple, reusable stuff. no business logic. may not import from ANY other high-level folder. may cross-import within the folder. put assets here (if needed)
- `entities`: models/entities. One folder per user-space entity such as "flashcard". May import from `db`, but nothing else.
- `features`: ways of interacting with entities. one folder per feature, following an entity-action (e.g. flashcard-manage) pattern. may NOT import one another. may ONLY import from `dumb` or `entities`, NEVER from other features.
- `pages`: One folder per page (a page is something used by the `router.ts` file). If functionality is ONLY used on a given page, put it in the page *folder* (avoid having just a single giant page file, split it up!), do not create features or meta-features that are only used by one single page.

No other high-level folders are allowed.
Do not use `index.ts` file reexporting components, simply export directly.

## Guidelines

- Keep design lean. Use cards, wrapper divs and containers ONLY when necessary
- Keep style consistent across the code base
- Setup eslint and ensure green linter (not by disabling it, but by writing clean code)
- Keep files, functions and classes short, with a single purpose, on one abstraction layer. Split complex functionality when called for.
- Do not hallucinate features I did not ask for
- Keep copy and micro-copy short and to the point. Avoid waffling, avoid marketing speak, and avoid labelling everything with triple redundancy.
- make sure UI looks neat. Always put a form input BELOW the label in a new line. Responsive design.
- KEEP. IT. SIMPLE.
- always run `npm run build` and `npm run lint:fix` to ensure everything is well done. Fix problems by writing clean code, not by disabling the linter.

## How To

If adding a new mini app, see `@add-a-new-app.md`
