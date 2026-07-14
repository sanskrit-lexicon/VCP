# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**VCP** is the development and correction repository for **Tāranātha Tarkavācaspati's *Vācaspatyam***, a vast indigenous Sanskrit→Sanskrit encyclopedic lexicon, within the [Cologne Digital Sanskrit Lexicon](https://www.sanskrit-lexicon.uni-koeln.de/) (CDSL).

- **Canonical source text**: [`csl-orig/v02/vcp/vcp.txt`](https://github.com/sanskrit-lexicon/csl-orig/blob/main/v02/vcp/vcp.txt) (48,636 entries) — corrections are applied to that file, not stored here.
- This repository holds **development artifacts**: corrections, markup, comparison, and per-issue working files.
- An indigenous encyclopaedic dictionary citing authorities through quotations and sigla (e.g. `pu0`, `avya0`) rather than Western `<ls>` markup. This repo also tracks the **VAC (Tirupati)** vs **VCP (Cologne)** edition comparison.

## Architecture

| Path | Purpose |
|---|---|
| `.github/` | GitHub Actions workflows + issue templates |
| `abbrevprep/` | Abbreviation-markup preparation |
| `alternateheadword/` | Alternate-headword extraction |
| `data/` | Working data files |
| `meld_regex/` | Regex rules for `meld` diff comparison |
| `vac-vcp-cmp1/` | VAC (Tirupati) vs VCP (Cologne) comparison |
| `vac-vcp-cmp1a/` | VAC vs VCP comparison (rev.) |
| `vac-vcp-cmp2/` | VAC vs VCP comparison (rev.) |
| `vcpte-vac/` | VCP-TE vs VAC comparison |
| `vcpte-vcp-cmp/` | VCP-TE vs VCP comparison |
| `verbs01/` | Verb identification: maps verb entries to MW roots, with Devanāgarī renderings |

## Key commands

Corrections follow the CDSL `updateByLine.py` pattern, applied against the csl-orig source:

```sh
python updateByLine.py <input> <changefile> <output>
```

Change-file format (paired lines; `;`-prefixed comments):

```
1234 old <original line>
1234 new <replacement line>
```
Supports `new` (replace), `ins` (insert after), `del` (delete). All files UTF-8 (**no BOM**).

## Data format

VCP entries use standard CDSL Sanskrit-lexicography markup. See [DATA_DICTIONARY.md](DATA_DICTIONARY.md) for the full tag reference.

| Tag | Role |
|---|---|
| `<L>NNNN<pc>PPP` | Entry begin, with print page-column ref |
| `<k1>`, `<k2>` | Primary / secondary headword (SLP1) |
| `<LEND>` | Entry end |
| `{#…#}` | Sanskrit text (SLP1) |
| `{%…%}` | Sanskrit gloss / italic display text |
| `¦` | Headword / definition separator |
| `<lex>…</lex>` | Lexical category |
| `<ls>…</ls>` | Literary source citation |

Annotated example — the first entry of `vcp.txt`:

```
<L>1<pc>0035,a<k1>a<k2>a
a¦ pu0 avati rakzati atati sAtatyena tizWatIti vA ava--ata--
vA qa . vizRO “akAro vizRuruddizwa ukArastu maheSvaraH .
makArastu smftobrahmA praRavastu trayAtmaka” iti . asya
(vizRoH) apatyam ata iY iH (kAmaH) asya (vizRoH)
patnI NIp I (lakzmIH) .
<LEND>
```

## Dependencies

- Python 3 (correction and comparison scripts).
- No build step in this repo; XML and web display are generated centrally from `csl-orig` via `csl-pywork`.

## GitHub Issue Conventions

This repository uses the Cologne dictionary-repo issue taxonomy. Every issue has exactly one **type**, one **severity**, and one **milestone**:

- **Type** (9): link-target, link-splitting, markup, text-correction, content-enhancement, encoding, scan-quality, bug, question
- **Severity** (3): minor, medium, hard
- **Milestone** (4): Dictionary to Book, Digitization Quality, Structured Data, Major Enhancements

See the [Cologne issue runbook](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-issue-runbook.md) for label definitions and the type→milestone mapping.