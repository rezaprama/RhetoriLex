# Writing-Skill Catalog

Use this catalog for guidance about what a passage or section should do. Use phrase-pattern search when the user already knows the move and needs adaptable wording.

## Groups

- Academic: research framing, literature writing, argumentation, thesis and dissertation, publication writing.
- Scientific: study framing, methods, results, discussion, scientific claim control.
- Integrity-preserving rewriting: paraphrasing.

The catalog contains 144 original English skill records. Each record provides a rhetorical objective, use cases, a worked English example, related phrase functions, related skills, an evidence warning, and a stable route. Indonesian assets localise interface labels and descriptions; they do not replace English patterns or examples.

## Offline retrieval

Search a name or ordinary intent:

```bash
python scripts/search.py "reporting uncertainty" --writing-skills --limit 3
```

Browse one substantive group:

```bash
python scripts/search.py --writing-skills --skill-group results-writing --limit 8
```

Retrieve one stable slug:

```bash
python scripts/search.py --skill-slug interpreting-null-results --json
```

Discover group IDs:

```bash
python scripts/search.py --list-writing-skill-groups
```

Add `--language id` when Indonesian interface labels help the user. The returned example remains canonical English.

## Selection discipline

Retrieve the smallest useful set. Check the record's evidence warning before adapting its example. Related phrase functions lead to pattern search; related skill IDs lead to adjacent planning guidance. A worked example demonstrates a move—it is not evidence and must not be copied as a factual claim.
