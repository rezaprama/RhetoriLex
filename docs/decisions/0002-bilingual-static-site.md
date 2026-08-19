# ADR 0002: Bilingual static site with generated canonical routes

- Status: Accepted
- Date: 2026-08-19

## Context

RhetoriLex needs indexable English and Bahasa Indonesia guidance, a searchable
phrase catalog, canonical writing-skill references, accessible theme and locale
preferences, and deployment on GitHub Pages. The site must work without a
client framework or runtime package installation. It must also keep interface
locale separate from the English language of released phrase patterns.

A single client-rendered page would make localized metadata, canonical URLs,
fragment references, and no-script access harder to verify. Root-domain asset
paths would break when the repository is hosted under the GitHub Pages project
base /RhetoriLex/.

## Decision

Use a deterministic Python standard-library builder at docs/build_site.py.
Generated HTML is committed. Running python docs/build_site.py --check verifies
that committed output matches source content and catalog data.

The builder produces:

- an accessible root locale chooser with noindex,follow, persisted locale
  selection, browser-language fallback, and visible English and Indonesian
  links;
- substantive multipage routes under /en/ and /id/;
- paired focused intent pages with localized slugs;
- eleven writing-skill group pages that consume the canonical structured
  catalog and expose stable fragment URLs for individual skills;
- unique titles, descriptions, canonical URLs, complete hreflang sets,
  localized social metadata, JSON-LD, and an absolute-URL sitemap;
- shared styles.css and app.js files with no external runtime dependency.

Every generated page calculates links relative to its directory. The phrase
explorer receives data-catalog-url as a page-relative path to
docs/data/phrases.json. Deep routes therefore remain inside the GitHub project
base and never request root-domain /data.

Locale preference uses rhetorilex.locale. Theme preference uses
rhetorilex.theme. These keys are independent. Changing the interface locale
does not translate, rewrite, or mutate English catalog patterns. Indonesian
writing-skill pages use maintained translations for names and descriptions,
while canonical examples and technical warnings remain marked as English.

## Consequences

Search engines and no-script readers receive substantive HTML rather than
doorway pages. Each skill has one canonical English group URL plus a stable
fragment. English and Indonesian alternates can be audited without running
JavaScript.

Catalog or content changes require rebuilding and committing generated HTML.
CI and the Pages workflow should run the builder in check mode before
deployment. The shared runtime remains small, but any explorer behavior change
must be tested against both locales and deep project-base routes.

The root chooser is intentionally excluded from search results. Localized home
pages are the indexable entry points.
