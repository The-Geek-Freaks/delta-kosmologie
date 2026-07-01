# GitHub Wiki

The curated GitHub Wiki is available at:

https://github.com/The-Geek-Freaks/delta-kosmologie/wiki

The versioned source pages live in [../wiki](../wiki). GitHub creates the
backing `.wiki.git` repository lazily: the first Wiki page must be saved once in
the GitHub web UI before local or CI-based sync can push into the Wiki remote.

## Pages

| Page | Purpose |
| --- | --- |
| Home | Main wiki landing page |
| Quick Start | Fast reader path through the framework |
| Framework Map | Layered explanation of RDelta, Babel Index, NEOTH, and tests |
| Babel Index | Score family, variables, and controls |
| NEOTH Pilot | Runtime experiment and telemetry targets |
| Falsification Standard | Claim boundary and invalid evidence |
| Visual Guide | Diagrams and source assets |
| Repository Map | File and artifact navigation |
| DeepWiki | External generated project reader |
| Glossary | Core terms |

## Sync

After the first page has been created in the GitHub UI, sync the versioned pages
with:

```bash
python scripts/publish_wiki.py
```

The same command is available as the manual `Sync GitHub Wiki` GitHub Actions
workflow.

## Relationship To Other Surfaces

- The README is the public landing page.
- The GitHub Wiki is the curated reader and navigation surface.
- DeepWiki is the generated external project reader.
- `llms.txt` and `codemeta.json` are machine-readable discovery surfaces.
