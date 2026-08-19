"""Dependency-free catalog loading, filtering, and ranking."""

from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from importlib import resources
import json
import random as random_module
import re
from typing import Any, Iterable, Mapping


_TOKEN_RE = re.compile(r"[a-z0-9]+")
_STRENGTH_ORDER = {"tentative": 0, "bounded": 1, "assertive": 2, "causal": 3}


def _normalize(text: str) -> str:
    return " ".join(_TOKEN_RE.findall(text.casefold()))


def _tokens(text: str) -> set[str]:
    return set(_TOKEN_RE.findall(text.casefold()))


@dataclass(frozen=True, slots=True)
class Entry:
    id: str
    function: str
    title: str
    template: str
    description: str
    stage: str
    disciplines: tuple[str, ...]
    claim_strength: str
    evidence_requirement: str
    causal_design_required: bool
    placeholders: tuple[str, ...]
    keywords: tuple[str, ...]
    notes: str
    risk: str
    provenance: Mapping[str, Any]
    version: int

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "Entry":
        return cls(
            id=str(value["id"]),
            function=str(value["function"]),
            title=str(value["title"]),
            template=str(value["template"]),
            description=str(value["description"]),
            stage=str(value["stage"]),
            disciplines=tuple(value["disciplines"]),
            claim_strength=str(value["claim_strength"]),
            evidence_requirement=str(value["evidence_requirement"]),
            causal_design_required=bool(value["causal_design_required"]),
            placeholders=tuple(value["placeholders"]),
            keywords=tuple(value["keywords"]),
            notes=str(value["notes"]),
            risk=str(value["risk"]),
            provenance=dict(value["provenance"]),
            version=int(value["version"]),
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "function": self.function,
            "title": self.title,
            "template": self.template,
            "description": self.description,
            "stage": self.stage,
            "disciplines": list(self.disciplines),
            "claim_strength": self.claim_strength,
            "evidence_requirement": self.evidence_requirement,
            "causal_design_required": self.causal_design_required,
            "placeholders": list(self.placeholders),
            "keywords": list(self.keywords),
            "notes": self.notes,
            "risk": self.risk,
            "provenance": dict(self.provenance),
            "version": self.version,
        }


@dataclass(frozen=True, slots=True)
class SearchResult:
    entry: Entry
    score: float
    match: str

    def as_dict(self) -> dict[str, Any]:
        value = self.entry.as_dict()
        value["score"] = round(self.score, 4)
        value["match"] = self.match
        return value


class Catalog:
    """Immutable in-memory view of the bundled catalog."""

    def __init__(
        self,
        entries: Iterable[Entry],
        taxonomy: Mapping[str, Any],
        contract: Mapping[str, Any],
    ) -> None:
        ordered = tuple(sorted(entries, key=lambda item: item.id))
        ids = [item.id for item in ordered]
        if len(ids) != len(set(ids)):
            raise ValueError("catalog contains duplicate ids")
        self.entries = ordered
        self.taxonomy = dict(taxonomy)
        self.contract = dict(contract)
        self._by_id = {item.id.casefold(): item for item in ordered}

    @classmethod
    def load(cls) -> "Catalog":
        root = resources.files("rhetorilex").joinpath("resources")
        catalog_data = json.loads(root.joinpath("catalog.json").read_text(encoding="utf-8"))
        taxonomy = json.loads(root.joinpath("taxonomy.json").read_text(encoding="utf-8"))
        contract = json.loads(root.joinpath("evidence_claim_contract.json").read_text(encoding="utf-8"))
        return cls((Entry.from_dict(row) for row in catalog_data["entries"]), taxonomy, contract)

    def get(self, entry_id: str) -> Entry:
        try:
            return self._by_id[entry_id.casefold()]
        except KeyError as exc:
            raise KeyError(f"unknown entry id: {entry_id}") from exc

    def _filtered(
        self,
        *,
        function: str | None = None,
        evidence: str | None = None,
        max_claim_strength: str | None = None,
        discipline: str | None = None,
        stage: str | None = None,
        risk: str | None = None,
    ) -> list[Entry]:
        if max_claim_strength is not None and max_claim_strength not in _STRENGTH_ORDER:
            raise ValueError(f"unknown claim strength: {max_claim_strength}")
        limit_strength = _STRENGTH_ORDER.get(max_claim_strength, 99)
        return [
            entry
            for entry in self.entries
            if (function is None or entry.function == function)
            and (evidence is None or entry.evidence_requirement == evidence)
            and (_STRENGTH_ORDER[entry.claim_strength] <= limit_strength)
            and (discipline is None or discipline in entry.disciplines or "general" in entry.disciplines)
            and (stage is None or entry.stage == stage or entry.stage == "general")
            and (risk is None or entry.risk == risk)
        ]

    def search(
        self,
        query: str,
        *,
        function: str | None = None,
        evidence: str | None = None,
        max_claim_strength: str | None = None,
        discipline: str | None = None,
        stage: str | None = None,
        risk: str | None = None,
        limit: int = 10,
        fuzzy: bool = True,
    ) -> list[SearchResult]:
        if limit < 1:
            raise ValueError("limit must be at least 1")
        normalized_query = _normalize(query)
        query_tokens = _tokens(query)
        candidates = self._filtered(
            function=function,
            evidence=evidence,
            max_claim_strength=max_claim_strength,
            discipline=discipline,
            stage=stage,
            risk=risk,
        )
        if not normalized_query:
            return [SearchResult(item, 0.0, "filter") for item in candidates[:limit]]

        ranked: list[SearchResult] = []
        for entry in candidates:
            id_text = _normalize(entry.id)
            title_text = _normalize(entry.title)
            template_text = _normalize(entry.template)
            keyword_text = _normalize(" ".join(entry.keywords))
            function_text = _normalize(entry.function)
            description_text = _normalize(entry.description)
            haystack = " ".join((title_text, template_text, keyword_text, function_text, description_text))
            haystack_tokens = _tokens(haystack)

            if normalized_query in {id_text, title_text, template_text}:
                score, match = 100.0, "exact"
            else:
                overlap = len(query_tokens & haystack_tokens)
                coverage = overlap / max(1, len(query_tokens))
                precision = overlap / max(1, len(haystack_tokens))
                phrase_bonus = 18.0 if normalized_query in haystack else 0.0
                keyword_bonus = 10.0 if normalized_query in keyword_text else 0.0
                lexical = coverage * 58.0 + precision * 7.0 + phrase_bonus + keyword_bonus
                ratio = 0.0
                if fuzzy:
                    ratio = max(
                        SequenceMatcher(None, normalized_query, title_text).ratio(),
                        SequenceMatcher(None, normalized_query, keyword_text).ratio(),
                        SequenceMatcher(None, normalized_query, function_text).ratio(),
                    )
                fuzzy_score = ratio * 40.0 if ratio >= 0.55 else 0.0
                score = lexical + fuzzy_score
                match = "lexical" if lexical >= fuzzy_score else "fuzzy"
            if score > 0:
                ranked.append(SearchResult(entry, score, match))

        ranked.sort(key=lambda item: (-item.score, item.entry.id))
        return ranked[:limit]

    def suggest(self, prefix: str, *, limit: int = 8) -> list[str]:
        if limit < 1:
            raise ValueError("limit must be at least 1")
        needle = _normalize(prefix)
        values: set[str] = set()
        for entry in self.entries:
            values.add(entry.function)
            values.add(entry.title)
            values.update(entry.keywords)
        ordered = sorted(values, key=lambda value: (_normalize(value), value))
        starts = [value for value in ordered if _normalize(value).startswith(needle)]
        if len(starts) < limit and needle:
            contains = [value for value in ordered if needle in _normalize(value) and value not in starts]
            starts.extend(contains)
        return starts[:limit]

    def random(
        self,
        *,
        seed: str | int | None = None,
        function: str | None = None,
        evidence: str | None = None,
        max_claim_strength: str | None = None,
        discipline: str | None = None,
        stage: str | None = None,
        risk: str | None = None,
    ) -> Entry:
        candidates = self._filtered(
            function=function,
            evidence=evidence,
            max_claim_strength=max_claim_strength,
            discipline=discipline,
            stage=stage,
            risk=risk,
        )
        if not candidates:
            raise LookupError("no entries match filters")
        return random_module.Random(seed).choice(candidates)

    def counts(self) -> dict[str, Any]:
        functions: dict[str, int] = {}
        evidence: dict[str, int] = {}
        risk: dict[str, int] = {}
        for entry in self.entries:
            functions[entry.function] = functions.get(entry.function, 0) + 1
            evidence[entry.evidence_requirement] = evidence.get(entry.evidence_requirement, 0) + 1
            risk[entry.risk] = risk.get(entry.risk, 0) + 1
        return {
            "entries": len(self.entries),
            "functions": dict(sorted(functions.items())),
            "evidence_requirements": dict(sorted(evidence.items())),
            "risk": dict(sorted(risk.items())),
        }
