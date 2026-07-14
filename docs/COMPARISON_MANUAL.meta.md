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
[H508-Fable_VCP_comparison_tooling_manual_10.07.26](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H508-Fable_VCP_comparison_tooling_manual_10.07.26.md)
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

## Intended use / known misuse

**Intended use:** an operator's runbook for the *live* VCP comparison/
collation workflow — running a VAC↔VCP meld correction round (§4.1),
recomputing diff metrics (§4.2), and rerunning the two side surveys
(`verbs01`, `abbrevprep`) and the alternate-headword pass. It is also the
authoritative pointer for which of the five comparison generations is live
(gen 5 only — §2) and which files are frozen archaeology.

**Known/likely misuse:**
- Treating the gen-1–4 folders (`vcpte-vcp-cmp/`, `vcpte-vac/`,
  `vac-vcp-cmp1/`, `vac-vcp-cmp1a/`) as runnable pipelines instead of frozen
  provenance — they are Python-2-era archaeology (§2, §7).
- Running `meld_regex/split_file.py` believing it is idempotent or safe to
  "refresh" — it overwrites years of hand-corrected chunks (§1, §5 row 1);
  there is still no mechanical guard against this (backlog item 2).
- Running `abbrevprep/redo.sh` expecting it to regenerate the abbreviation
  survey — it is a broken copy-paste of `verbs01`'s tail and will instead
  attempt (and fail at) verb-filter commands (§4.4, §5 row 3, §7 defect 1).
- Copying `vcp_corrected_file.txt` straight over
  `csl-orig/v02/vcp/vcp.txt` as an org agent — that `cp`-based path
  (`carry_changes_to_cslorig.sh`) is the upstream-maintainer-only pattern;
  org agents must go through the change-file + correction-queue route
  (§4.1 step 5).
- Redistributing VAC-derived data (`vcpte-vac/vac_input.txt` or anything
  downstream of it) without honoring its CC BY-NC-SA non-commercial clause
  (§7 never-touch list).
- Reading the root Excel-algo notes
  (`Tirupati-vs-Cologe-Excel-comparison-algo.txt`) as UTF-8 — they are
  cp1251 Russian and render as mojibake without the correct encoding (§5).

## Maintenance & sunset plan

The manual is kept alive by whoever next runs a meld correction round or
touches `meld_regex/`, `vac-vcp-cmp2/`, `verbs01/`, `abbrevprep/`, or
`alternateheadword/` in the [VCP](https://github.com/sanskrit-lexicon/VCP)
repo — there is no dedicated bot or CI job; it is maintained the same way as
the rest of the repo's docs, by the operator/contributor of record for a
given session (see Audience above). Sunset trigger: if the live workflow is
ever superseded by a new comparison generation (a "gen 6"), or the VAC↔VCP
correction programme is formally closed out (all meld rounds complete, no
further csl-orig drift to reconcile per [issue #24](https://github.com/sanskrit-lexicon/VCP/issues/24)),
this manual and its subject document should be marked `retired` here and in
the manual's own header, with a pointer to whatever replaces it (or a note
that the workflow ended and the folders are now archaeology like gen 1–4).
Until then it stays `active` and gets updated in place whenever a described
command, file path, or defect changes.

## Deprecation status

`active`

## Related documents

- [README.md](https://github.com/sanskrit-lexicon/VCP/blob/main/README.md) — repo overview, issue inventory, front-matter (prefaces) docs
- [DATA_DICTIONARY.md](https://github.com/sanskrit-lexicon/VCP/blob/main/DATA_DICTIONARY.md) — markup tag reference
- [CLAUDE.md](https://github.com/sanskrit-lexicon/VCP/blob/main/CLAUDE.md) — repo guide + issue taxonomy
- [csl-corrections correction workflow](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md) — the canonical delivery path this manual defers to

## Revision history

| Date | Change | By |
|---|---|---|
| 11-07-2026 | Initial version (H508) | Fable 5 (`claude-fable-5`) |
| 11-07-2026 | template v2 backfill (H663) | Sonnet 5 (`claude-sonnet-5`) |

---

_Dr. Mārcis Gasūns_
