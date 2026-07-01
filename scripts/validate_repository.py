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
    if isinstance(system, dict) and system.get("repo") != NEOTH_URL:
        failures.append("Window example must point to the NEOTH repository")


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
    validate_codemeta(failures, topics)
    validate_html_head(failures)
    validate_examples(failures)
    validate_language_surface(failures)

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print(f"Repository validation passed: {len(REQUIRED_FILES)} artifacts, {len(topics)} topics.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
