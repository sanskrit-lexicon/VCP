# COMPARISON_MANUAL.md — metadoc

_Created: 11-07-2026 · Last updated: 11-07-2026_

Companion record for
[docs/COMPARISON_MANUAL.md](https://github.com/sanskrit-lexicon/VCP/blob/main/docs/COMPARISON_MANUAL.md).

## Purpose

The operator manual for VCP's comparison/collation tooling: the five
generations of Tirupati-vs-Cologne comparison (which one is live and how to
run a meld correction round), the delivery contract back to csl-orig, and the
three side workflows (verbs01 verb→MW mapping, abbrevprep sigla survey,
alternate-headword extraction).

## Audience

- An operator running a VAC↔VCP meld correction round or recomputing the
  diff metrics.
- A contributor picking up verbs01 / abbrevprep / alternateheadword work.
- Anyone tempted to rerun a frozen gen-1–4 script or `split_file.py`
  (the manual exists largely to stop that).

## Provenance

Authored 11-07-2026 by Fable 5 (`claude-fable-5`) under handoff
[H508-Fable_VCP_comparison_tooling_manual_10.07.26](https://github.com/gasyoun/Uprava/blob/main/handoffs/H508-Fable_VCP_comparison_tooling_manual_10.07.26.md)
(the H501–H531 per-repo manuals programme, Litpam-Indexator MANUAL.md gold
standard). Commands and formats read from the per-folder readmes
(`meld_regex/readme.md`, `vac-vcp-cmp2/readme.md`, `verbs01/readme.txt`,
`abbrevprep/readme.txt`, `alternateheadword/readme.md`, the gen-1–4
`readme.org`/`readme.txt` files) and the scripts themselves — none invented.
The four §7 defects were observed in the committed files.

## Ranked improvement backlog

| # | Item | Status |
|---|---|---|
| 1 | Fix or delete the broken [abbrevprep/redo.sh](https://github.com/sanskrit-lexicon/VCP/blob/main/abbrevprep/redo.sh) (copy-pasted verbs01 tail, missing mode arg, wrong header comment) | open |
| 2 | Add a mechanical guard to `meld_regex/split_file.py` (refuse to run if the target split dir is non-empty) — today the DO-NOT-REDO warning is prose-only | open |
| 3 | Document the reconciliation step for csl-orig drift (live `vcp.txt` moving under a long meld round — the §5 standing hazard, [issue #24](https://github.com/sanskrit-lexicon/VCP/issues/24)) as an exact procedure | open |
| 4 | Remove committed `.pyc` files and `vcpte-vac/readme.org~`; add both patterns to `.gitignore` | open |
| 5 | Re-encode (or annotate in-place) the cp1251 Russian Excel-algo notes with an explicit encoding marker | open |

## Known limitations

- The gen-1–4 folders are described at lineage level, not script-by-script —
  they are frozen archaeology; their internal readmes remain the reference
  if anyone ever needs to re-derive them.
- The VAC↔VCP correction *content* decisions (which side is right when the
  editions disagree) are scholarly judgment outside this manual's scope; it
  documents the mechanics only.
- `redo_copy.sh` (verbs01 → Cologne web tree) is a maintainer-side step not
  reproducible from this repo alone.

## Related documents

- [README.md](https://github.com/sanskrit-lexicon/VCP/blob/main/README.md) — repo overview, issue inventory, front-matter (prefaces) docs
- [DATA_DICTIONARY.md](https://github.com/sanskrit-lexicon/VCP/blob/main/DATA_DICTIONARY.md) — markup tag reference
- [CLAUDE.md](https://github.com/sanskrit-lexicon/VCP/blob/main/CLAUDE.md) — repo guide + issue taxonomy
- [csl-corrections correction workflow](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md) — the canonical delivery path this manual defers to

## Revision history

| Date | Change | By |
|---|---|---|
| 11-07-2026 | Initial version (H508) | Fable 5 (`claude-fable-5`) |

---

_Dr. Mārcis Gasūns_
