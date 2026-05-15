# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**VCP** is the corrections and research repository for the Cologne digitization of Vachaspatyam (*Vācaspatyam*) — Tara Nath Tarkavachaspati's comprehensive Sanskrit dictionary (6 volumes, 1873–1884). The canonical source lives in `csl-orig/v02/vcp/vcp.txt`. This is one of the largest CDSL dictionaries.

## Architecture

| Directory/File | Purpose |
|---|---|
| `verbs01/` | Root identification: maps VCP verb entries to MW root spellings, identifies prefixed verbs |
| `data/` | Data files for various correction workflows |
| `abbrevprep/` | Abbreviation preparation and markup |
| `alternateheadword/` | Alternate headword analysis |
| `meld_regex/` | Meld/regex-based correction workflows |
| `vac-vcp-cmp1/` / `vac-vcp-cmp1a/` | Comparison between Vachaspatyam (vac) and VCP digitizations |
| `vac-vcp-cmp2/` | Extended comparison (phase 2) |
| `vcpte-vac/` | VCPte (Telugu edition) vs Vachaspatyam comparison |
| `vcpte-vcp-cmp/` | VCPte vs VCP digitization comparison |

### Verb root pipeline (`verbs01/`)

Identifies VCP verb entries and maps them to MW equivalents with preverb (upasarga) resolution. Cross-referenced with SKD verb analysis ([SKD issue #9](https://github.com/sanskrit-lexicon/SKD/issues/9)).

### Tirupati vs Cologne comparison

The repo contains comparative data between the Tirupati (2013) edition of Vachaspatyam and the Cologne digitization, including Excel and algorithm results.

Issues and corrections are tracked via the [GitHub issue tracker](https://github.com/sanskrit-lexicon/VCP/issues).

## Common Commands

### Apply line-level corrections (standard pattern)
```bash
python updateByLine.py <input_file> <changein_file> <output_file>
```

### Rebuild and validate XML (from `csl-pywork/v02/`)
```bash
sh generate_dict.sh vcp ../../VCPScan/2020
sh xmlchk_xampp.sh vcp
```

## Dependencies

- **Python 3**
- **vcp.txt** — in `$BASE/cologne/csl-orig/v02/vcp/vcp.txt`
