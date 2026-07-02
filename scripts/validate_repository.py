#!/usr/bin/env python3
"""Validate the public repository surface without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
NEOTH_URL = "https://github.com/The-Geek-Freaks/NEOTH"
DELTA_REPO_URL = "https://github.com/The-Geek-Freaks/delta-kosmologie"
WIKI_URL = "https://github.com/The-Geek-Freaks/delta-kosmologie/wiki"
PAGES_URL = "https://the-geek-freaks.github.io/delta-kosmologie/"
DEEPWIKI_URL = "https://deepwiki.com/The-Geek-Freaks/delta-kosmologie"

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "CITATION.cff",
    "codemeta.json",
    "llms.txt",
    "docs/index.html",
    "docs/overview.md",
    "docs/visual-guide.md",
    "docs/neoth-integration.md",
    "docs/neoth-discovery-bridge.md",
    "docs/repository-settings.md",
    "docs/wiki.md",
    "paper/delta-cosmology-v1.0.md",
    "paper/delta-cosmology-v1.0.html",
    "paper/delta-kosmologie-v1.0.pdf",
    "paper/delta-kosmologie-v1.0.txt",
    "protocols/babel-index.md",
    "protocols/pilot-b-neoth.md",
    "schemas/neoth-babel-event.schema.json",
    "schemas/neoth-babel-window.schema.json",
    "examples/neoth-babel-event.example.json",
    "examples/neoth-babel-window.example.json",
    "assets/delta-cosmology-overview.svg",
    "assets/delta-cosmology-hero-v3.svg",
    "assets/rdelta-framework-map.svg",
    "assets/babel-index-pipeline.svg",
    "assets/claim-boundary.svg",
    "assets/social-preview.svg",
    "assets/social-preview.png",
    "metadata/repository-metadata.yml",
    "metadata/repository-topics.txt",
    ".github/workflows/sync-wiki.yml",
    "scripts/publish_wiki.py",
    "wiki/Home.md",
    "wiki/_Sidebar.md",
    "wiki/_Footer.md",
    "wiki/Quick-Start.md",
    "wiki/Framework-Map.md",
    "wiki/Babel-Index.md",
    "wiki/NEOTH-Pilot.md",
    "wiki/Falsification-Standard.md",
    "wiki/Visual-Guide.md",
    "wiki/Repository-Map.md",
    "wiki/DeepWiki.md",
    "wiki/Glossary.md",
]


class HeadParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.in_title = False
        self.metas: dict[tuple[str, str], str] = {}
        self.links: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        if tag == "title":
            self.in_title = True
        if tag == "meta":
            if "name" in data:
                self.metas[("name", data["name"])] = data.get("content", "")
            if "property" in data:
                self.metas[("property", data["property"])] = data.get("content", "")
        if tag == "link" and "rel" in data:
            self.links[data["rel"]] = data.get("href", "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data.strip()


def text_files() -> Iterable[Path]:
    suffixes = {".cff", ".html", ".json", ".md", ".svg", ".txt", ".yaml", ".yml"}
    ignored = {".git", "__pycache__", "node_modules", ".venv"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        if any(part in ignored for part in path.parts):
            continue
        yield path


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text(encoding="utf-8")


def load_json(rel_path: str) -> object:
    return json.loads(read(rel_path))


def local_link_targets(text: str) -> list[str]:
    targets = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
    targets += re.findall(r"(?:href|src)=[\"']([^\"']+)[\"']", text)
    return targets


def is_external(target: str) -> bool:
    return target.startswith(("http://", "https://", "mailto:", "data:", "#"))


def validate_links(failures: list[str]) -> None:
    for path in text_files():
        if path.suffix.lower() not in {".html", ".md", ".txt", ".yml", ".yaml"}:
            continue
        text = path.read_text(encoding="utf-8")
        for raw_target in local_link_targets(text):
            target = raw_target.strip().split()[0]
            if is_external(target):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            decoded = urllib.parse.unquote(target)
            resolved = (path.parent / decoded).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                failures.append(f"{path.relative_to(ROOT)} links outside repo: {raw_target}")
                continue
            if not resolved.exists():
                failures.append(f"{path.relative_to(ROOT)} has missing link: {raw_target}")


def validate_json(failures: list[str]) -> None:
    for path in text_files():
        if path.suffix.lower() == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                failures.append(f"{path.relative_to(ROOT)} is invalid JSON: {exc}")


def validate_svg(failures: list[str]) -> None:
    for rel_path in [
        "assets/delta-cosmology-overview.svg",
        "assets/delta-cosmology-hero-v3.svg",
        "assets/rdelta-framework-map.svg",
        "assets/babel-index-pipeline.svg",
        "assets/claim-boundary.svg",
        "assets/social-preview.svg",
    ]:
        try:
            ET.parse(ROOT / rel_path)
        except ET.ParseError as exc:
            failures.append(f"{rel_path} is invalid XML/SVG: {exc}")


def validate_topics(failures: list[str]) -> list[str]:
    topics = [
        line.strip()
        for line in read("metadata/repository-topics.txt").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    if not (1 <= len(topics) <= 20):
        failures.append(f"GitHub topics count must be 1..20, got {len(topics)}")
    for topic in topics:
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,49}", topic):
            failures.append(f"Invalid GitHub topic: {topic}")
    joined_surfaces = "\n".join(
        [
            read("README.md"),
            read("metadata/repository-metadata.yml"),
            read("docs/repository-settings.md"),
            read("codemeta.json"),
            read("llms.txt"),
        ]
    )
    for topic in topics:
        if topic not in joined_surfaces:
            failures.append(f"Topic not present across discovery surfaces: {topic}")
    return topics


def validate_required_files(failures: list[str]) -> None:
    for rel_path in REQUIRED_FILES:
        path = ROOT / rel_path
        if not path.exists():
            failures.append(f"Missing required file: {rel_path}")
        elif path.is_file() and path.stat().st_size == 0:
            failures.append(f"Required file is empty: {rel_path}")


def validate_neoth_backlinks(failures: list[str]) -> None:
    surfaces = [
        "README.md",
        "docs/overview.md",
        "docs/neoth-integration.md",
        "docs/neoth-discovery-bridge.md",
        "protocols/pilot-b-neoth.md",
        "metadata/repository-metadata.yml",
        "llms.txt",
        "codemeta.json",
    ]
    for rel_path in surfaces:
        if NEOTH_URL not in read(rel_path):
            failures.append(f"Missing NEOTH backlink in {rel_path}")
    if DELTA_REPO_URL not in read("llms.txt"):
        failures.append("llms.txt must include the canonical repository URL")


def validate_deepwiki_links(failures: list[str]) -> None:
    surfaces = [
        "README.md",
        "docs/index.html",
        "docs/visual-guide.md",
        "docs/repository-settings.md",
        "metadata/repository-metadata.yml",
        "llms.txt",
        "codemeta.json",
    ]
    for rel_path in surfaces:
        if DEEPWIKI_URL not in read(rel_path):
            failures.append(f"Missing DeepWiki link in {rel_path}")


def validate_wiki_links(failures: list[str]) -> None:
    surfaces = [
        "README.md",
        "docs/index.html",
        "docs/repository-settings.md",
        "docs/wiki.md",
        "metadata/repository-metadata.yml",
        "llms.txt",
        "codemeta.json",
    ]
    for rel_path in surfaces:
        if WIKI_URL not in read(rel_path):
            failures.append(f"Missing GitHub Wiki link in {rel_path}")


def validate_wiki_source(failures: list[str]) -> None:
    wiki_dir = ROOT / "wiki"
    pages = {path.stem for path in wiki_dir.glob("*.md")}
    for required in [
        "Home",
        "_Sidebar",
        "_Footer",
        "Quick-Start",
        "Framework-Map",
        "Babel-Index",
        "NEOTH-Pilot",
        "Falsification-Standard",
        "Visual-Guide",
        "Repository-Map",
        "DeepWiki",
        "Glossary",
    ]:
        if required not in pages:
            failures.append(f"Missing wiki source page: wiki/{required}.md")

    wiki_link_pattern = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
    for path in wiki_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("|") and stripped.endswith("|") and "[[" in stripped:
                failures.append(
                    f"{path.relative_to(ROOT)}:{line_number} uses GitHub Wiki link syntax inside a table"
                )
        for match in wiki_link_pattern.finditer(text):
            label, target = match.groups()
            page = target or label
            if page not in pages:
                failures.append(f"{path.relative_to(ROOT)} links missing wiki page: {page}")


def validate_codemeta(failures: list[str], topics: list[str]) -> None:
    data = load_json("codemeta.json")
    if not isinstance(data, dict):
        failures.append("codemeta.json must be a JSON object")
        return
    expected = {
        "name": "Delta Cosmology",
        "codeRepository": DELTA_REPO_URL,
        "url": PAGES_URL,
        "license": "https://spdx.org/licenses/CC-BY-4.0",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            failures.append(f"codemeta.json {key!r} must be {value!r}")
    keywords = data.get("keywords", [])
    if not isinstance(keywords, list):
        failures.append("codemeta.json keywords must be a list")
        return
    for topic in topics:
        if topic not in keywords:
            failures.append(f"codemeta.json missing keyword/topic: {topic}")


def validate_html_head(failures: list[str]) -> None:
    parser = HeadParser()
    parser.feed(read("docs/index.html"))
    if "Delta Cosmology" not in parser.title:
        failures.append("docs/index.html title must include Delta Cosmology")
    for key in [
        ("name", "description"),
        ("name", "keywords"),
        ("property", "og:title"),
        ("property", "og:description"),
        ("property", "og:image"),
        ("name", "twitter:card"),
    ]:
        if not parser.metas.get(key):
            failures.append(f"docs/index.html missing meta {key[0]}={key[1]}")
    if parser.links.get("canonical") != PAGES_URL:
        failures.append("docs/index.html canonical URL must match the GitHub Pages URL")


def validate_examples(failures: list[str]) -> None:
    event_schema = load_json("schemas/neoth-babel-event.schema.json")
    window_schema = load_json("schemas/neoth-babel-window.schema.json")
    event = load_json("examples/neoth-babel-event.example.json")
    window = load_json("examples/neoth-babel-window.example.json")
    if not isinstance(event_schema, dict) or not isinstance(window_schema, dict):
        failures.append("Schema files must be JSON objects")
        return
    if not isinstance(event, dict) or not isinstance(window, dict):
        failures.append("Example files must be JSON objects")
        return

    for field in event_schema.get("required", []):
        if field not in event:
            failures.append(f"Event example missing required field: {field}")
    event_types = event_schema.get("properties", {}).get("event_type", {}).get("enum", [])
    if event.get("event_type") not in event_types:
        failures.append("Event example event_type is not in schema enum")

    for field in window_schema.get("required", []):
        if field not in window:
            failures.append(f"Window example missing required field: {field}")
    features = window.get("features", {})
    if not isinstance(features, dict):
        failures.append("Window example features must be an object")
        return
    for symbol in ["C", "K", "M", "A", "V", "D", "H"]:
        value = features.get(symbol)
        if not isinstance(value, (int, float)):
            failures.append(f"Window example feature {symbol} must be numeric")
    system = window.get("system", {})
    NEOTH_SLUG = "The-Geek-Freaks/NEOTH"
    if isinstance(system, dict) and system.get("repo") != NEOTH_SLUG:
        failures.append(
            f"Window example system.repo must be the slug {NEOTH_SLUG!r}, not a full URL"
        )

    # Check example schema_version matches the schema's declared const.
    schema_version_const = (
        window_schema.get("properties", {})
        .get("schema_version", {})
        .get("const")
    )
    if schema_version_const is not None and window.get("schema_version") != schema_version_const:
        failures.append(
            f"Window example schema_version {window.get('schema_version')!r} "
            f"does not match schema const {schema_version_const!r}"
        )

    # Recompute B_neoth_log (natural log, ratio form) and assert within 1e-3.
    import math as _math
    ftr = window.get("features", {})
    if all(isinstance(ftr.get(s), (int, float)) for s in ["C", "K", "M", "A", "V", "D", "H"]):
        C_, K_, M_, A_, V_, D_, H_ = (
            float(ftr["C"]), float(ftr["K"]), float(ftr["M"]),
            float(ftr["A"]), float(ftr["V"]),
            float(ftr["D"]), float(ftr["H"]),
        )
        scores = window.get("candidate_scores", {})
        if scores.get("B_neoth_log") is not None:
            try:
                expected_log = (
                    _math.log(C_) + _math.log(K_) + _math.log(M_)
                    + _math.log(A_ / D_) + _math.log(V_ / H_)
                )
                actual_log = float(scores["B_neoth_log"])
                if abs(actual_log - expected_log) > 1e-3:
                    failures.append(
                        f"Window example B_neoth_log {actual_log} differs from recomputed "
                        f"natural-log ratio-form value {expected_log:.4f} by more than 1e-3"
                    )
            except (ValueError, ZeroDivisionError):
                failures.append("Window example B_neoth_log could not be recomputed (zero/negative feature)")

        # Recompute B_neoth_bottleneck: min(C,K,M,A,V) / max(D,H).
        if scores.get("B_neoth_bottleneck") is not None:
            expected_bn = min(C_, K_, M_, A_, V_) / max(D_, H_)
            actual_bn = float(scores["B_neoth_bottleneck"])
            if abs(actual_bn - expected_bn) > 1e-3:
                failures.append(
                    f"Window example B_neoth_bottleneck {actual_bn} differs from recomputed "
                    f"value {expected_bn:.4f} by more than 1e-3"
                )

    # Check epsilon-rule tag when present.
    scores = window.get("candidate_scores", {})
    epsilon_rule = scores.get("B_neoth_mult_epsilon_rule")
    CANONICAL_EPSILON_TAG = "0.01_median_buffer_ratio_calibration"
    if epsilon_rule is not None and epsilon_rule != CANONICAL_EPSILON_TAG:
        failures.append(
            f"Window example B_neoth_mult_epsilon_rule {epsilon_rule!r} "
            f"must be {CANONICAL_EPSILON_TAG!r}"
        )

    # Check all checked window examples that carry B_neoth_log use natural log
    # and match the declared schema version. Additional examples can stay
    # exploratory, but published NEOTH windows must not drift silently.
    for rel_path in [
        "examples/neoth-babel-window.example.json",
        "examples/neoth-babel-window.negative-control.example.json",
    ]:
        if not (ROOT / rel_path).exists():
            continue
        candidate = load_json(rel_path)
        if not isinstance(candidate, dict):
            failures.append(f"{rel_path} must be a JSON object")
            continue
        if schema_version_const is not None and candidate.get("schema_version") != schema_version_const:
            failures.append(
                f"{rel_path} schema_version {candidate.get('schema_version')!r} "
                f"does not match schema const {schema_version_const!r}"
            )
        candidate_scores = candidate.get("candidate_scores", {})
        if not isinstance(candidate_scores, dict):
            failures.append(f"{rel_path} candidate_scores must be an object")
            continue
        log_base = candidate_scores.get("B_neoth_log_base")
        if candidate_scores.get("B_neoth_log") is not None and log_base != "e":
            failures.append(f"{rel_path} B_neoth_log_base must be 'e' when B_neoth_log is present")
        elif log_base is not None and log_base != "e":
            failures.append(f"{rel_path} B_neoth_log_base must be 'e', got {log_base!r}")

        candidate_features = candidate.get("features", {})
        if isinstance(candidate_features, dict) and all(
            isinstance(candidate_features.get(s), (int, float)) for s in ["C", "K", "M", "A", "V", "D", "H"]
        ) and candidate_scores.get("B_neoth_log") is not None:
            try:
                C_, K_, M_, A_, V_, D_, H_ = (
                    float(candidate_features["C"]),
                    float(candidate_features["K"]),
                    float(candidate_features["M"]),
                    float(candidate_features["A"]),
                    float(candidate_features["V"]),
                    float(candidate_features["D"]),
                    float(candidate_features["H"]),
                )
                expected_log = (
                    _math.log(C_) + _math.log(K_) + _math.log(M_)
                    + _math.log(A_ / D_) + _math.log(V_ / H_)
                )
                actual_log = float(candidate_scores["B_neoth_log"])
                if abs(actual_log - expected_log) > 1e-3:
                    failures.append(
                        f"{rel_path} B_neoth_log {actual_log} differs from recomputed "
                        f"natural-log ratio-form value {expected_log:.4f} by more than 1e-3"
                    )
            except (ValueError, ZeroDivisionError):
                failures.append(f"{rel_path} B_neoth_log could not be recomputed")

        candidate_epsilon_rule = candidate_scores.get("B_neoth_mult_epsilon_rule")
        if candidate_epsilon_rule is not None and candidate_epsilon_rule != CANONICAL_EPSILON_TAG:
            failures.append(
                f"{rel_path} B_neoth_mult_epsilon_rule {candidate_epsilon_rule!r} "
                f"must be {CANONICAL_EPSILON_TAG!r}"
            )


def validate_markdown_formula_artifacts(failures: list[str]) -> None:
    score_text = read("examples/babel-score-computation.md")
    stale_values = ["-" + "2.9073", "\u2212" + "2.9073"]
    for stale_value in stale_values:
        if stale_value in score_text:
            failures.append(f"examples/babel-score-computation.md contains stale B_neoth_log value {stale_value}")

    old_formula = re.compile(r"D\s*[×*]\s*H\s*\+\s*(?:ε|epsilon)", re.IGNORECASE)
    if old_formula.search(score_text):
        failures.append("examples/babel-score-computation.md contains stale D*H epsilon denominator")
    if re.search(r"median\s*\(\s*D\s*[×*]\s*H", score_text, re.IGNORECASE):
        failures.append("examples/babel-score-computation.md contains stale multiplicative epsilon rule")
    if 'B_neoth_log_base = "e"' not in score_text:
        failures.append('examples/babel-score-computation.md must state B_neoth_log_base = "e"')

    stale_score_name = "B_" + "NEOTH"
    for rel_path in ["README.md", "docs/neoth-integration.md", "protocols/pilot-b-neoth.md"]:
        if stale_score_name in read(rel_path):
            failures.append(f"{rel_path} contains stale generic NEOTH score naming")
    stale_paper_phrase = "five " + "independent factors"
    if stale_paper_phrase in read("paper/delta-cosmology-v1.0.md"):
        failures.append("paper/delta-cosmology-v1.0.md contains stale multiplicative-form wording")


def validate_collapse_label_consistency(failures: list[str]) -> None:
    event_schema = load_json("schemas/neoth-babel-event.schema.json")
    window_schema = load_json("schemas/neoth-babel-window.schema.json")
    if not isinstance(event_schema, dict) or not isinstance(window_schema, dict):
        failures.append("Schema files must be JSON objects")
        return

    schema_enum = (
        event_schema.get("properties", {})
        .get("collapse_label", {})
        .get("enum", [])
    )
    schema_labels = {label for label in schema_enum if isinstance(label, str)}
    if not schema_labels:
        failures.append("schemas/neoth-babel-event.schema.json collapse_label enum must not be empty")
        return

    label_properties = (
        window_schema.get("properties", {})
        .get("labels", {})
        .get("properties", {})
    )
    for field_name in ["collapse_within_30m_kind", "collapse_kind"]:
        enum_values = label_properties.get(field_name, {}).get("enum", [])
        window_labels = {label for label in enum_values if isinstance(label, str)}
        if window_labels != schema_labels:
            failures.append(
                f"schemas/neoth-babel-window.schema.json {field_name} labels "
                f"{sorted(window_labels)} do not match event schema labels {sorted(schema_labels)}"
            )

    definitions_text = read("protocols/collapse-label-definitions.md")
    definition_labels = set(
        re.findall(r"^## Label \d+: `([^`]+)`", definitions_text, flags=re.MULTILINE)
    )
    if definition_labels != schema_labels:
        failures.append(
            "protocols/collapse-label-definitions.md labels "
            f"{sorted(definition_labels)} do not match event schema labels {sorted(schema_labels)}"
        )
    stale_subsumed_note = "Subsumed `" + "tool_selection_failure`"
    if stale_subsumed_note in definitions_text:
        failures.append(
            "protocols/collapse-label-definitions.md still subsumes tool_selection_failure "
            "instead of defining it as a canonical label"
        )

    for rel_path in ["protocols/pilot-b-neoth.md", "docs/neoth-integration.md"]:
        text = read(rel_path)
        missing = sorted(label for label in schema_labels if f"`{label}`" not in text)
        if missing:
            failures.append(f"{rel_path} is missing canonical collapse labels: {', '.join(missing)}")


def validate_language_surface(failures: list[str]) -> None:
    banned_terms = [
        "Praeformalismus",
        "Erledigt",
        "Gemacht",
        "Codex",
        "connector",
        "prepared workspace",
        "push is blocked",
        "workspace ZIP",
    ]
    for path in text_files():
        text = path.read_text(encoding="utf-8")
        for term in banned_terms:
            if term in text:
                failures.append(f"{path.relative_to(ROOT)} contains non-English residue: {term}")


def main() -> int:
    failures: list[str] = []
    validate_required_files(failures)
    validate_json(failures)
    validate_links(failures)
    validate_svg(failures)
    topics = validate_topics(failures)
    validate_neoth_backlinks(failures)
    validate_deepwiki_links(failures)
    validate_wiki_links(failures)
    validate_wiki_source(failures)
    validate_codemeta(failures, topics)
    validate_html_head(failures)
    validate_examples(failures)
    validate_markdown_formula_artifacts(failures)
    validate_collapse_label_consistency(failures)
    validate_language_surface(failures)

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print(f"Repository validation passed: {len(REQUIRED_FILES)} artifacts, {len(topics)} topics.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
