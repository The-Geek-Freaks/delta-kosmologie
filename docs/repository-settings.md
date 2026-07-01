# Repository Settings Checklist

Some GitHub repository settings cannot be represented as versioned files:
About text, homepage, topics, Pages, and social preview.

Use the following values in GitHub's repository settings.

## About

Description:

```text
Open RDelta/Babel Index framework for LLM agents and world-systems: detect context degeneration, agent loops, tool fragility, and collapse with NEOTH.
```

Website:

```text
https://the-geek-freaks.github.io/delta-kosmologie/
```

Use the GitHub repository URL only until Pages is enabled:

```text
https://github.com/The-Geek-Freaks/delta-kosmologie
```

DeepWiki:

```text
https://deepwiki.com/The-Geek-Freaks/delta-kosmologie
```

## Topics

Recommended GitHub topics:

```text
llm-agents
ai-agents
agentic-ai
ai-observability
agent-observability
llm-evaluation
ai-safety
complex-systems
systems-theory
telemetry
collapse-prediction
babel-index
rdelta
neoth
tool-use
context-degeneration
agent-loops
semantic-collapse
llm-observability
runtime-telemetry
```

## Social Preview

Use:

```text
assets/social-preview.png
```

Source file:

```text
assets/social-preview.svg
```

## GitHub Pages

Optional:

1. Settings -> Pages
2. Source: `Deploy from a branch`
3. Branch: `main`
4. Folder: `/docs`

This will publish `docs/index.html` as a compact project landing page.

Expected Pages URL:

```text
https://the-geek-freaks.github.io/delta-kosmologie/
```

## NEOTH Reciprocal Link

Add the backlink snippet from [docs/neoth-discovery-bridge.md](neoth-discovery-bridge.md)
to the NEOTH README so both repositories reinforce each other in GitHub search.

## Machine-Readable Discovery

Keep these files in sync with repository settings:

- [../llms.txt](../llms.txt)
- [../codemeta.json](../codemeta.json)
- [../metadata/repository-metadata.yml](../metadata/repository-metadata.yml)
- [../metadata/repository-topics.txt](../metadata/repository-topics.txt)
