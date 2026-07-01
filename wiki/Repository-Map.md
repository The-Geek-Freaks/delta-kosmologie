# Repository Map

| Path | Purpose |
| --- | --- |
| README.md | Public landing page |
| docs/ | Overview, falsification, framework, visual guide, settings |
| paper/ | Markdown, HTML, TXT, and PDF paper artifacts |
| protocols/ | Babel Index and NEOTH pilot protocols |
| schemas/ | Machine-readable JSON schemas |
| examples/ | Example NEOTH telemetry payloads |
| assets/ | SVG diagrams and social-preview image |
| metadata/ | Repository description, topics, and discovery metadata |
| scripts/ | Local repository validation |
| .github/ | CI, issue templates, pull request template |

## Quality Gate

Run this locally before changing repository surfaces:

```bash
python scripts/validate_repository.py
```

The validator checks required artifacts, local links, JSON metadata, SVG
well-formedness, telemetry examples, NEOTH backlinks, DeepWiki links, and topic
consistency.
