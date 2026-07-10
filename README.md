# VCP — *Vācaspatyam* (1873–1884)

_Created: 21-01-2014 · Last updated: 11-07-2026_

Development and correction repository for **Tāranātha Tarkavācaspati's *Vācaspatyam***, a vast indigenous Sanskrit→Sanskrit encyclopedic lexicon, part of the [Cologne Digital Sanskrit Lexicon](https://www.sanskrit-lexicon.uni-koeln.de/) (CDSL). The canonical source text lives in [`csl-orig/v02/vcp/vcp.txt`](https://github.com/sanskrit-lexicon/csl-orig/blob/master/v02/vcp/vcp.txt) (48,636 entries); this repository holds the development, correction, and enrichment work.

An indigenous encyclopaedic dictionary citing authorities through quotations and sigla (e.g. `pu0`, `avya0`) rather than Western `<ls>` markup. This repo also tracks the **VAC (Tirupati)** vs **VCP (Cologne)** edition comparison.

## Documentation

- [docs/COMPARISON_MANUAL.md](https://github.com/sanskrit-lexicon/VCP/blob/main/docs/COMPARISON_MANUAL.md) — **operator manual** for the comparison/collation tooling: the live VAC↔VCP meld correction workflow, the diff metrics, verbs01, abbrevprep, alternate headwords, and the delivery contract back to csl-orig.
- [CLAUDE.md](CLAUDE.md) — repository guide and data-format reference.
- [DATA_DICTIONARY.md](DATA_DICTIONARY.md) — markup tag reference.
- [CONTRIBUTING.md](CONTRIBUTING.md) · [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## Contents

| Path | Purpose |
|---|---|
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
| `prefaces/` | Front-matter OCR (title pages, publisher's note, dedication, preface, contents) + EN/RU translations — see [Front matter](#front-matter-prefaces) below |

## Timeline

| Period | Activity |
|---|---|
| 2014 | Repository activity begins (first tracked issues) |
| 2015–2021 | Ongoing corrections, markup, and comparison work |
| 2026-05 | Issue taxonomy, citation metadata, documentation |
| 2026-06 | Front-matter OCR + EN/RU translation of the prefaces (`prefaces/`) |

## Projects & Milestones

| Milestone | Open | Closed | Total |
|---|---|---|---|
| Dictionary to Book | 0 | 0 | 0 |
| Digitization Quality | 6 | 8 | 14 |
| Structured Data | 8 | 2 | 10 |
| Major Enhancements | 6 | 1 | 7 |
| **Total** | **20** | **11** | **31** |

```mermaid
pie showData
  title VCP issues by milestone
  "Digitization Quality" : 14
  "Structured Data" : 10
  "Major Enhancements" : 7
```

## Issues

```mermaid
pie showData
  title VCP issues by type
  "content-enhancement" : 7
  "text-correction" : 7
  "question" : 6
  "bug" : 5
  "markup" : 4
  "encoding" : 1
  "scan-quality" : 1
```

### Open

| # | Title | Type | Severity | Milestone |
|---|---|---|---|---|
| 3 | Link to Preface | content-enhancement | medium | Major Enhancements |
| 5 | Vachaspatyam-Doubles | text-correction | minor | Digitization Quality |
| 7 | Progress in alternate headword extraction | markup | minor | Structured Data |
| 9 | All dhatu entries | content-enhancement | medium | Major Enhancements |
| 10 | All Dhatu Entries: verbs01 | content-enhancement | medium | Major Enhancements |
| 11 | abbreviation preparation | markup | minor | Structured Data |
| 12 | vac-vcp-cmp2 | question | minor | Structured Data |
| 14 | VAC (TE) vs. VCP (Cologne) | content-enhancement | medium | Major Enhancements |
| 15 | Meld as a diff viewer for VAC-VCP comparision | question | minor | Structured Data |
| 17 | Suggestions from meta2 | text-correction | minor | Digitization Quality |
| 18 | meld-prep: 'ai'/'au' | encoding | minor | Digitization Quality |
| 19 | vac2a - picture data in TE | bug | minor | Digitization Quality |
| 20 | pUrbb vs. pUrvv | bug | minor | Digitization Quality |
| 22 | Patterns to be handled later | question | minor | Structured Data |
| 23 | Debatable items | question | minor | Structured Data |
| 24 | VAC vs VCP comparision tracker | content-enhancement | medium | Major Enhancements |
| 25 | Query regarding any addenda / corrigenda to Vachaspatyam | question | minor | Structured Data |
| 27 | aNgirAuvAca | markup | minor | Structured Data |
| 29 | Spacing issues in VCP | bug | minor | Digitization Quality |
| 31 | docs-pass: VCP documentation review | content-enhancement | medium | Major Enhancements |

### Solved

| # | Title | Type | Severity | Milestone |
|---|---|---|---|---|
| 1 | Tirupati vs. Cologne Edition Text Comparison | content-enhancement | medium | Major Enhancements |
| 2 | Renaming VCP to VCPTE | question | minor | Structured Data |
| 4 | herasva> heramba | text-correction | minor | Digitization Quality |
| 6 | Tirupati v. Cologne example | text-correction | minor | Digitization Quality |
| 8 | Broken link -- from IITS Koeln home page | bug | minor | Digitization Quality |
| 13 | New VCP scans | scan-quality | minor | Digitization Quality |
| 16 | Correction of {??} missing text in vcp.txt | text-correction | minor | Digitization Quality |
| 21 | print changes pages 34-40 | text-correction | minor | Digitization Quality |
| 26 | print changes 41-50 | text-correction | minor | Digitization Quality |
| 28 | pending 'rbb' in vcp.txt | bug | minor | Digitization Quality |
| 30 | [markup] Minor vcp.txt Markup Oddities | markup | minor | Structured Data |

## Labels

### Type labels

| Label | Meaning |
|---|---|
| `link-target` | Click-throughs from `<ls>` abbreviations to scanned PDF pages |
| `link-splitting` | Splitting combined `SOURCE N,N` refs into per-page links |
| `markup` | Normalising XML tag content |
| `text-correction` | Corrections to Sanskrit/Sanskrit definitions or headwords |
| `content-enhancement` | New material or structural additions beyond correction |
| `encoding` | SLP1/IAST transcoding, character normalisation |
| `scan-quality` | Replacing blurry/skewed/missing scan pages |
| `bug` | Broken links, XML errors, broken downloads |
| `question` | Scholarly questions requiring research |

### Severity labels

| Label | Meaning |
|---|---|
| `minor` | Targeted fix — a handful of lines or a single file |
| `medium` | Standard unit of work — one batch of corrections |
| `hard` | Large effort spanning many sources or files |

## Contributors

| Contributor | Commits |
|---|---|
| drdhaval2785 | 66 |
| funderburkjim | 35 |
| gasyoun (Mārcis Gasūns) | 26 |

## Source

- **Author**: Tarkavācaspati, Tāranātha
- **Title**: *Vācaspatyam*
- **Place / Publisher**: Calcutta
- **Year(s)**: 1873–1884
- **Volumes**: 6 fascicles
- **Language pair**: Sanskrit → Sanskrit
- **Size (CDSL headword index)**: 48,636 entries
- **License (digital edition)**: CC BY-SA 4.0
- See [CITATION.cff](CITATION.cff) for machine-readable citation.

## Encoding

- UTF-8 (NFC) throughout.
- Sanskrit text in SLP1 transliteration, wrapped in `{#…#}`; Sanskrit gloss / italic display text in `{%…%}`.
- Devanāgarī and IAST display forms are generated at display time, not stored in the source.

## Usage example

Applying a correction to the real first entry of [`vcp.txt`](https://github.com/sanskrit-lexicon/csl-orig/blob/master/v02/vcp/vcp.txt) with `updateByLine.py` (root [`CLAUDE.md`](https://github.com/sanskrit-lexicon/csl-orig/blob/master/CLAUDE.md) "Shared correction pattern"). The real current line 2 (entry 1, headword `a`) reads:

```
a¦ pu0 avati rakzati atati sAtatyena tizWatIti vA ava--ata--
```

A change file pairs the old/new lines by line number (illustrating a hypothetical sandhi-spacing fix, `ava--ata--` → `ava-ata-`):

```
; change_vcp_example.txt
2 old a¦ pu0 avati rakzati atati sAtatyena tizWatIti vA ava--ata--
2 new a¦ pu0 avati rakzati atati sAtatyena tizWatIti vA ava-ata-
```

```sh
python updateByLine.py vcp.txt change_vcp_example.txt vcp_corrected.txt
```

Illustrative only (no such correction is queued) — the "before" line is the real, current `csl-orig/v02/vcp/vcp.txt` line 2.

## How it works

```mermaid
flowchart LR
  S["Print scan"] -->|keyboarding| O["csl-orig/v02/vcp/vcp.txt"]
  O -->|updateByLine.py| C["change_*.txt corrections"]
  C --> O
  O --> V["verbs01/ verb identification"]
  O -->|csl-pywork build| X["vcp.xml"]
  X --> A["csl-app web display"]
```

## Front matter (`prefaces/`)

OCR of the dictionary's **front matter** — title pages, publisher's note, dedication, preface, and contents — from the [Cologne csldoc scans](https://sanskrit-lexicon.uni-koeln.de/scans/csldev/csldoc/build/dictionaries/prefaces/vcppref.html), with English and Russian translations and consolidated single-file editions. 7 pages, mixed-language: the first title page and publisher page are **Sanskrit / Devanāgarī**; the second title page, publisher's note, dedication, preface, and contents are **English** (19th-c. spellings preserved). Digitizer running-header/footer stamps were omitted.

File conventions: `vcpprefNN.md` (source language) · `vcpprefNN.en.md` (English) · `vcpprefNN.ru.md` (Russian). Consolidated editions:

- [`prefaces/vcppref_all.sa.md`](https://github.com/sanskrit-lexicon/VCP/blob/master/prefaces/vcppref_all.sa.md) — source language (Sanskrit + English)
- [`prefaces/vcppref_all.en.md`](https://github.com/sanskrit-lexicon/VCP/blob/master/prefaces/vcppref_all.en.md) — English
- [`prefaces/vcppref_all.ru.md`](https://github.com/sanskrit-lexicon/VCP/blob/master/prefaces/vcppref_all.ru.md) — Russian
- In-folder index: [`prefaces/README.md`](https://github.com/sanskrit-lexicon/VCP/blob/master/prefaces/README.md) · builder [`prefaces/build_combined.py`](https://github.com/sanskrit-lexicon/VCP/blob/master/prefaces/build_combined.py)

**Signatures & dates found**: title pages dated Vikrama Saṃvat 2018 / A.D. 1962 (Chowkhamba reprint); dedication to H.H. the Maharajah of Vizianagaram, signed by the author Tāranātha Tarkavācaspati; preface signed **H. Woodrow, M.A.**, citing Govt. of Bengal sanction letters of 1866 and 1870.

<details>
<summary><strong>OCR run notes (2026-06-22)</strong> — cost, timing, and technical lessons</summary>

Produced by the `/cologne-preface-ocr` skill (vision OCR + translation). Process retrospective, not part of the deliverable.

**Cost.** This was a **resume** run: a prior session had already OCR'd all 7 source pages, written all 7 `.ru.md`, and the two Sanskrit pages' `.en.md`. This session, synchronous (no subagents), did the remaining work: wrote the five English-source `.en.md` (verbatim English reproductions of pages 03–07), demoted stray in-body title-page H1s to H2 in 9 page files, built the three consolidated editions, and authored the READMEs. Main thread only — ≈90k tokens (no native-resolution OCR crops needed this turn; the scans were already transcribed).

**Time.** Wall-clock ≈8 min, single foreground thread.

**Technical lessons (reusable):**
1. Mixed-language front matter ⇒ `source_lang` is per-page. For English-source pages the base `.md` *is* the English; this run still materialized `.en.md` copies for them so `build_combined.py`'s `en` pass (which `continue`s on missing `.en.md`) emits a **complete** English edition rather than dropping pages.
2. Title pages repeat the dictionary title as a second `# ` heading and the dedication uses `# VIZIANAGARAM` as a display line. `build_combined.py` strips only the *first* H1, so these collide with the page-level H2 — demote them to `##` in the source page before building (H2 count must equal 1 TOC + 7 pages = 8).

</details>

---
*Issue taxonomy and documentation per the [Cologne issue runbook](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/runbook/cologne-issue-runbook.md).*

_Dr. Mārcis Gasūns_
