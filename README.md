# VCP - Vachaspatyam

<!-- BEGIN MANUAL: overview -->
VCP is the working repository for the Cologne digitization of
Vachaspatyam.  The canonical dictionary text lives in
[`csl-orig/v02/vcp/vcp.txt`](https://github.com/sanskrit-lexicon/csl-orig/blob/master/v02/vcp/vcp.txt);
this repository keeps the analysis notes, comparison files, scripts, and issue
work used to improve that source.

## Primary data

| Item | Location | Notes |
|---|---|---|
| Canonical CDSL source | `csl-orig/v02/vcp/vcp.txt` | Target of accepted corrections. |
| Local data extracts | `data/`, `all_list.txt`, `Vachaspatyam_b6_proof_1673-06-01-14.xlsx` | Working lists and proofing material. |
| Printed-source notes | `Vachaspatyam-Preface_Tirupati2013.pdf`, `vAcaspatyAbhidhAne.txt`, `vAcaspatyapariyojanAmadhikRtya.txt` | Source and project context. |
| Dictionary metadata | `DATA_DICTIONARY.md`, `CITATION.cff` | General CDSL markup and citation metadata. |

## Directories

| Path | Purpose |
|---|---|
| `abbrevprep/` | Abbreviation extraction and display experiments. |
| `alternateheadword/` | Bracketed-word and alternate-headword analysis. |
| `data/` | Headword and supporting data used by local scripts. |
| `vac-vcp-cmp1/`, `vac-vcp-cmp1a/`, `vac-vcp-cmp2/` | VAC/VCP comparison work. |
| `vcpte-vac/`, `vcpte-vcp-cmp/` | VCPTE comparison notes and scripts. |
| `verbs01/` | Verb and preverb identification against MW verb data. |
| `meld_regex/` | Regex and comparison aids. |

## Major workflows

| Workflow | Paths | Result |
|---|---|---|
| Abbreviation review | `abbrevprep/` | Markdown/text summaries of abbreviations in `vcp.txt`. |
| Alternate-headword extraction | `alternateheadword/` | `validated.txt` and `nonvalidated.txt` style candidate lists. |
| Verb and preverb work | `verbs01/` | VCP verb list, MW correspondences, and parsed upasarga/preverb output. |
| VAC/VCP comparison | `vac-vcp-*`, `vcpte-*` | Comparison logs used to decide possible corrections or structural differences. |

## How work is done

Most work follows Jim's change-file pattern:

```text
csl-orig source -> local temp/extract file -> script -> log/change file -> manual review -> csl-orig update
```

Do not edit the canonical source silently.  A correction should point back to a
local `readme.*`, issue note, generated change file, or comparison log.

## Common commands

Examples from existing notes:

```sh
python abbrev0.py deva,md,1 ../../../cologne/csl-orig/v02/vcp/vcp.txt abbrev0_deva_all.md abbrev0_deva_all.txt
python vcp_verb_filter.py ../vcp.txt vcp_verb_filter_exclude.txt vcp_verb_filter_include.txt vcp_verb_filter.txt
python vcp_verb_filter_map.py vcp_verb_filter.txt mwverbs1.txt vcp_verb_filter_map.txt
python preverb1.py slp1 temp_vcp.txt vcp_verb_filter_map.txt mwverbs1.txt vcp_preverb1.txt
```

Several older notes assume an XAMPP or Cologne-style sibling checkout.  Adjust
relative paths before re-running them.

## Data format

VCP uses standard CDSL line markup: `<L>` entry id, `<k1>` primary headword,
`<k2>` alternate headword, `<pc>` page/column, `<ls>` literary source, and
`<ab>` abbreviation.  Sanskrit is normally stored in SLP1 in the source layer;
display scripts derive Devanagari/roman forms later.

## Current status / open questions

- `alternateheadword/validated.txt` style output is considered high-confidence,
  but nonvalidated candidates need manual review before integration.
- `verbs01/` deliberately creates temporary VCP variants for preverb parsing;
  decide case by case whether a temporary recoding should become a print-source
  correction.
- Many paths in older notes were written for a different local checkout layout.
<!-- END MANUAL: overview -->

## Issues

This repository uses the Sanskrit Lexicon unified issue taxonomy with:
- **9 type labels**: link-target, link-splitting, markup, text-correction, content-enhancement, encoding, scan-quality, bug, question
- **3 severity levels**: minor, medium, hard
- **4 milestones**: Dictionary to Book, Digitization Quality, Structured Data, Major Enhancements

## GitHub Issue Conventions

All issues follow the unified taxonomy. See [CLAUDE.md](CLAUDE.md) for details.

---
*Updated by Cologne Issue Runbook*
