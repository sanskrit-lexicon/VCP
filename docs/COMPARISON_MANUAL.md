# VCP Comparison & Collation Tooling Manual

_Created: 11-07-2026 · Last updated: 11-07-2026_

The operator manual for VCP's comparison/collation tooling: the
Tirupati-vs-Cologne edition comparison in its five generations (and which one
is actually live), the meld-based correction workflow that feeds fixes back
to `csl-orig`, the `verbs01` verb-to-MW-root identification chain, the
`abbrevprep` sigla survey, and the alternate-headword extraction. Written so
a new operator can run each workflow end-to-end without reading the source.

Companion metadoc: [docs/COMPARISON_MANUAL.meta.md](https://github.com/sanskrit-lexicon/VCP/blob/main/docs/COMPARISON_MANUAL.meta.md).

---

## 1. Cheat-sheet — the live workflows on one screen

```bash
# A. VAC-vs-VCP correction round (meld_regex/ — THE live comparison workflow)
cd meld_regex
meld vac2_split/vac_00001 vcp2_split/vcp_00001    # visual diff, correct BOTH sides
#   …repeat per 500-line chunk pair…
cat vac2_split/vac_* > vac3.txt                   # reassemble + sanity-compare
cat vcp2_split/vcp_* > vcp3.txt                   #   against vac-vcp-cmp2/{vac2,vcp2}.txt
python3 merge_corrected_file_with_vcp.py \
    ../../../cologne/csl-orig/v02/vcp/vcp.txt ../vac-vcp-cmp2/vcp2.txt vcp_corrected_file.txt
# delivery to csl-orig: see §4.1 — org agents go through the correction queue,
# NEVER a direct copy/push (carry_changes_to_cslorig.sh is the upstream-
# maintainer pattern only)

# B. Recompute the difference metrics (vac-vcp-cmp2/)
pip install simplediff
cd vac-vcp-cmp2 && sh redo.sh     # len2.py → hwdiff.tsv + len2.tsv → *.html

# C. Rebuild verb identification (verbs01/)
cd verbs01 && sh redo.sh          # needs csl-orig at ../../../cologne/csl-orig

# D. Regenerate the abbreviation survey (abbrevprep/)
cd abbrevprep
python abbrev0.py deva,md,1 ../../../cologne/csl-orig/v02/vcp/vcp.txt \
    abbrev0_deva_all.md abbrev0_deva_all.txt
```

**The one command you must NEVER run:** `split_file.py` in `meld_regex/`
(§5, row 1) — the split chunks carry years of hand-corrections; re-splitting
overwrites them.

## 2. The two editions, and five generations of comparing them

Two independent digitizations of Tāranātha Tarkavācaspati's *Vācaspatyam*
exist:

- **VCP** — the Cologne edition:
  [csl-orig/v02/vcp/vcp.txt](https://github.com/sanskrit-lexicon/csl-orig/blob/main/v02/vcp/vcp.txt)
  (48,636 entries, SLP1, UTF-8), the CDSL canonical text.
- **VAC** — Peter Scharf's reformatted version of the **Tirupati edition**
  (received 2014 as `vac_input.txt`; license **CC BY-NC-SA** — note the
  *non-commercial* clause, stricter than the repo's own license). "VCPTE"
  in the oldest folders is an earlier e-text of the same Tirupati edition.

Because the two were keyboarded independently, their disagreements locate
typos in *either* edition — the comparison is a correction engine, not just
a report. The work spans five generations; **only the last one is live**:

| Generation | Folder | Year | What it contributed | Status |
|---|---|---|---|---|
| 1 | [vcpte-vcp-cmp/](https://github.com/sanskrit-lexicon/VCP/tree/main/vcpte-vcp-cmp) | 2014 | First VCPTE↔VCP headword alignment (`hw_cmp7.py` + force files); encoding converters (`cp1252_to_utf8.py`, `hk_to_slp1.py`) | archaeology |
| 2 | [vcpte-vac/](https://github.com/sanskrit-lexicon/VCP/tree/main/vcpte-vac) | 2014 | Scharf's `vac_input.txt` ingested; the headword-block correspondence `hwcmpvcp.txt` (VAC block ↔ VCP block) | archaeology |
| 3 | [vac-vcp-cmp1/](https://github.com/sanskrit-lexicon/VCP/tree/main/vac-vcp-cmp1) | 2014 | `len1.py` squash-length statistics over the correspondence (48,059 matches; 2,269 lines differing by ≥10 chars); interactive `match1c.py` inspection | archaeology |
| 4 | [vac-vcp-cmp1a/](https://github.com/sanskrit-lexicon/VCP/tree/main/vac-vcp-cmp1a) | 2021 | Rebased onto the 2021 `vcp.txt`; `make_vcp1.py`/`make_vcp2.py` strip metalines to make the two texts line-comparable; hiatus + picture-data change files | archaeology |
| 5 | [vac-vcp-cmp2/](https://github.com/sanskrit-lexicon/VCP/tree/main/vac-vcp-cmp2) + [meld_regex/](https://github.com/sanskrit-lexicon/VCP/tree/main/meld_regex) | 2021–live | `len2.py` per-headword diff metrics + the meld chunk-correction workflow | **LIVE** |

There is also a root-level Excel prototype of the same idea
([Tirupati-vs-Cologe-Excel-comparison-algo.txt](https://github.com/sanskrit-lexicon/VCP/blob/main/Tirupati-vs-Cologe-Excel-comparison-algo.txt)
+ `.xlsm`) — VBA + regex notes, prose in **Russian, cp1251-encoded** (it
renders as mojibake if opened as UTF-8; see §5).

## 3. Data-flow diagram

```
csl-orig/v02/vcp/vcp.txt  (Cologne, canonical)      vac_input.txt (Scharf/Tirupati, 2014)
        │                                                   │
        │  gen 4: make_vcp1.py / make_vcp2.py               │  gen 1–3 alignment
        │  (strip <L>/<LEND> metalines,                     │  (hwcmpvcp.txt block
        │   line-align to vac2.txt)                         │   correspondence)
        ▼                                                   ▼
   vac-vcp-cmp2/vcp2.txt  ◄────── compared with ──────  vac-vcp-cmp2/vac2.txt
        │                                                   │
        │            len2.py (simplediff)                   │
        ├──► hwdiff.tsv  (headword entry-count mismatches)  │
        ├──► len2.tsv    (per-headword <ins>/<del> diffs)   │
        │      └─ tsv_to_html.py → hwdiff.html / len2.html  │
        │                                                   │
        │  split_file.py (2022, ONE-TIME — never rerun)     │
        ▼                                                   ▼
   meld_regex/vcp2_split/vcp_*  ◄──── meld ────►  meld_regex/vac2_split/vac_*
        │        (human corrects BOTH sides, chunk by chunk)
        ▼
   cat vcp2_split/vcp_* > vcp3.txt → verified → copied over vac-vcp-cmp2/vcp2.txt
        │
        ▼
   merge_corrected_file_with_vcp.py  (re-attach metalines from live vcp.txt)
        ▼
   vcp_corrected_file.txt  ──► corrections into csl-orig  (§4.1 delivery rules)

SIDE WORKFLOWS (all read vcp.txt directly):
  verbs01/     vcp verb entries → MW roots     (§4.3)
  abbrevprep/  sigla survey (pu0, avya0, …)    (§4.4)
  alternateheadword/  bracketed alt headwords  (§4.5)
```

## 4. Step-by-step operator walkthrough

### 4.1 The live correction round (`meld_regex/`)

The methodology of record is
[meld_regex/readme.md](https://github.com/sanskrit-lexicon/VCP/blob/main/meld_regex/readme.md)
(+ discussion in [issue #15](https://github.com/sanskrit-lexicon/VCP/issues/15)):

1. The 2022 one-time split put `vac-vcp-cmp2/{vac2,vcp2}.txt` into 500-line
   chunks: `vac2_split/vac_*` and `vcp2_split/vcp_*`. **Do not re-run
   `split_file.py`** — the chunks have since been hand-corrected; a re-split
   overwrites that work (the readme says so twice).
2. Open corresponding chunk pairs in **meld** and correct **both** sides —
   a VAC typo is fixed in the VAC chunk, a VCP typo in the VCP chunk.
   `regex_list.txt` collects normalization regexes used during this pass.
3. Reassemble and verify: `cat vac2_split/vac_* > vac3.txt` (same for vcp),
   diff `vac3.txt` against `vac-vcp-cmp2/vac2.txt`; if sane, copy over.
4. Re-attach the Cologne metalines:
   `python3 merge_corrected_file_with_vcp.py <path-to-csl-orig>/v02/vcp/vcp.txt ../vac-vcp-cmp2/vcp2.txt vcp_corrected_file.txt`
   — this walks the live `vcp.txt` and substitutes the corrected body lines,
   producing a full replacement candidate.
5. **Delivery to csl-orig — two different worlds:**
   [carry_changes_to_cslorig.sh](https://github.com/sanskrit-lexicon/VCP/blob/main/meld_regex/carry_changes_to_cslorig.sh)
   ends with a literal `cp vcp_corrected_file.txt …/csl-orig/v02/vcp/vcp.txt`
   — that is the **upstream-maintainer pattern** (Dhaval/Jim commit to
   csl-orig directly). **Org agents must never do that**: prepare the diff as
   change files, XML-validate locally, and route through the correction queue
   / consolidated batch PR per the canonical
   [correction workflow](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md)
   (change-file format: paired `old`/`new` lines keyed by line number,
   applied by `updateByLine.py`).

### 4.2 Recomputing the difference metrics (`vac-vcp-cmp2/`)

```bash
pip install simplediff        # the one third-party dependency in this repo
cd vac-vcp-cmp2 && sh redo.sh
```

[len2.py](https://github.com/sanskrit-lexicon/VCP/blob/main/vac-vcp-cmp2/len2.py)
compares `vcp1.txt` vs `vac1.txt` after aggressive normalization (drop
non-alphabetics, strip XML-like tags, drop `#N` homonym numbers, keep one
parse of `x(y)z` alternates, concatenate multi-entry headwords) and writes:

- **`hwdiff.tsv`** — headwords whose *entry counts* differ
  (`headword ⟶ countInVcp ⟶ countInVac`); a `0` on either side is a missing
  or misspelled headword in that edition (e.g. `AgrahAyARika 0 1` = a VAC
  error).
- **`len2.tsv`** — per-headword body diffs, VAC shown with `<ins>`/`<del>`
  tags relative to VCP, for fast error location in long entries.

`tsv_to_html.py` renders each TSV to a browsable HTML
([hwdiff.html](https://github.com/sanskrit-lexicon/VCP/blob/main/vac-vcp-cmp2/hwdiff.html),
[len2.html](https://github.com/sanskrit-lexicon/VCP/blob/main/vac-vcp-cmp2/len2.html)).
Rerun after each meld round to measure convergence.

### 4.3 Verb identification (`verbs01/`)

Maps VCP's verb entries to MW roots, producing the per-verb table with
Devanāgarī renderings. One driver runs the whole chain
([verbs01/redo.sh](https://github.com/sanskrit-lexicon/VCP/blob/main/verbs01/redo.sh)),
which expects csl-orig at `../../../cologne/csl-orig` (edit `CSLORIG=` at the
top for your layout):

1. `mwverb.py` — harvest MW's verb entries from the sibling `mw.txt` →
   `mwverbs.txt` (k1, L, category, class-pada, prefix parse);
2. `mwverbs1.py` — merge same-headword records; categories collapse to
   `verb` / `preverb` → `mwverbs1.txt`;
3. `updateByLine.py` + `preverb_manualByLine.txt` — build **`temp_vcp.txt`**,
   a throwaway variant of `vcp.txt` in which ~48 nonstandard upasarga
   spellings (`<HI>parA--nirAkAraRe`) are recoded to the standard
   `parA + nirAkAraRe` form so downstream parsing needs only one pattern
   (deliberately NOT a print change to `vcp.txt` itself);
4. `vcp_verb_filter.py` + hand-kept `_exclude`/`_include` lists — select
   VCP's verb entries so they exactly agree with the known dhātu set;
5. `vcp_verb_filter_map.py` — align VCP verb spellings to MW spellings
   (historic stats: 2,243 mapped, 1,985 of them spelled differently,
   34 unmapped);
6. `preverb1.py` — parse upasarga compounds via
   `re.search(r'^<HI>([a-zA-Z +]+) [+] ', line)` with sandhi (`upa + A` →
   `upA`); all cases + frequencies in `vcp_upasarga_parse.txt`;
7. `verb1.py` run twice (`slp1`, then `deva`) → **`vcp_verb1.txt`** +
   **`vcp_verb1_deva.txt`**, the final tables. `redo_copy.sh` then copies
   them to the Cologne web tree (maintainer step).

### 4.4 Abbreviation survey (`abbrevprep/`)

VCP cites authorities with indigenous **sigla** (`pu0`, `avya0`, …: a
Devanāgarī abbreviation + `0`) rather than `<ls>` markup.
[abbrev0.py](https://github.com/sanskrit-lexicon/VCP/blob/main/abbrevprep/abbrev0.py)
surveys them:

```bash
python abbrev0.py roman,md,100 <csl-orig>/v02/vcp/vcp.txt abbrev0_roman_100.md
python abbrev0.py deva,md,1    <csl-orig>/v02/vcp/vcp.txt abbrev0_deva_all.md abbrev0_deva_all.txt
```

Mode string = `script,format,min-frequency` (per the invocations of record
in [abbrevprep/readme.txt](https://github.com/sanskrit-lexicon/VCP/blob/main/abbrevprep/readme.txt)):
`deva,md,1` lists every siglum with Devanāgarī display; `roman,md,100` only
those occurring ≥100 times. Output = the committed `abbrev0_*.md` frequency
tables (split into `_part1`/`_part2` for GitHub rendering). This is the raw
material for eventual abbreviation markup. ⚠️ Ignore
[abbrevprep/redo.sh](https://github.com/sanskrit-lexicon/VCP/blob/main/abbrevprep/redo.sh)
— it is a broken copy-paste (§5, row 3); use the readme.txt invocations
above.

### 4.5 Alternate headwords (`alternateheadword/`)

VCP prints variant headwords in brackets — `x(y)z` — and this pass
([alternateheadword/readme.md](https://github.com/sanskrit-lexicon/VCP/blob/main/alternateheadword/readme.md),
[issue #7](https://github.com/sanskrit-lexicon/VCP/issues/7)) extracts them:
`hw1_dhaval.py` splits bracket-bearing headwords (`bracketwords.txt`, mid vs
end bracket), decides whether the bracketed string replaces the preceding or
following part (Levenshtein distance + known letter-exchange patterns like
b/v, S/s), and checks candidates against the org-wide headword list
[data/hw1.txt](https://github.com/sanskrit-lexicon/VCP/blob/main/data/hw1.txt):
a hit lands in `validated.txt` (safe to integrate), a miss in
`nonvalidated.txt` (manual review; method codes 1–6 name the rule that fired,
`404` = no decision). Root-level
[47046-vachaspatyam-words-w-brackets.txt](https://github.com/sanskrit-lexicon/VCP/blob/main/47046-vachaspatyam-words-w-brackets.txt)
and the `Vachaspatyam_b6_proof_*` pair are earlier bracket-headword harvests
of the same phenomenon.

## 5. Symptom → cause → cure

| Symptom | Cause | Cure |
|---|---|---|
| Hand-corrections in `meld_regex/*_split/` gone | Someone re-ran `split_file.py`, which regenerates the chunks from `vac2.txt`/`vcp2.txt` | **Prevention only** — the readme's DO-NOT-REDO is the sole guard. Recover from git history (`git checkout -- vac2_split vcp2_split`) |
| `ModuleNotFoundError: simplediff` | The one pip dependency (len2.py) | `pip install simplediff` |
| `verbs01/redo.sh` / abbrev runs fail with "No such file … csl-orig" | `CSLORIG="../../../cologne/csl-orig"` assumes the maintainer's XAMPP layout | Clone csl-orig and edit `CSLORIG=` (or symlink) to your actual path |
| `abbrevprep/redo.sh` runs verb-filter commands and fails | The script is a defective copy-paste: its abbrev0 line is missing the `mode` argument and its tail is verbs01's redo block (header comment even says `…/skd/verbs01`) | Don't run it; use the `abbrev0.py <mode>,md,<n> …` invocations from `readme.txt` (§4.4) |
| `Entry init error: duplicate L` from abbrev0.py/parseheadline | The input vcp.txt has a duplicated `<L>` id (corruption or a bad merge) | Fix the input; the scripts refuse to continue by design |
| `Tirupati-vs-Cologe-Excel-comparison-algo.txt` is mojibake | Russian prose in cp1251, not UTF-8 | Open with cp1251 (`iconv -f cp1251`); do not "fix" the file to UTF-8 without checking the `.xlsm` still matches |
| `vac_input.txt`-era files unreadable as UTF-8 | Scharf-era files were Latin-1/cp1252; that's why `latin1_to_utf8.py` / `cp1252_to_utf8.py` exist in the gen-1/2 folders | Convert a copy; the committed gen-3+ files are already UTF-8 |
| `merge_corrected_file_with_vcp.py` output looks misaligned vs vcp.txt | The live `vcp.txt` moved since `vcp2.txt` was derived (csl-orig gets independent corrections) | Diff the two first; reconcile csl-orig's newer changes into the chunk files before merging (this is the workflow's standing hazard — see [issue #24](https://github.com/sanskrit-lexicon/VCP/issues/24)) |
| Want to rerun gen 1–4 scripts | They're Python-2-era in places (`print` statements, `.pyc` files committed) and their inputs are frozen snapshots | Don't — they are archaeology (§2); the live workflow is gen 5 |

## 6. Glossary

| Term | Meaning |
|---|---|
| VCP | The Cologne digitization of Vācaspatyam (Calcutta 1873–1884), canonical in csl-orig |
| VAC | Peter Scharf's reformatted version of the Tirupati edition (2014, CC BY-NC-SA) |
| VCPTE | The earlier raw e-text of the Tirupati edition (gen-1 folders) |
| Tirupati edition | The 20th-c. re-edition of Vācaspatyam whose independent keyboarding makes the comparison possible |
| siglum (`pu0`, `avya0`) | VCP's indigenous abbreviation style: Devanāgarī abbreviation + `0`, citing authorities/categories instead of `<ls>` markup |
| squash / squashline | Gen-3 normalization: an entry's text reduced to bare letters for length comparison (`len1.py`) |
| metaline | The `<L>NNNN<pc>PPP<k1>…<k2>…` entry-header line; stripped to make VCP line-comparable with VAC, re-attached on merge |
| meld | The GUI three-way diff tool used for the chunk-by-chunk visual comparison |
| upasarga | Verbal prefix (`upa`, `parA`, …); `preverb1.py` parses them, with sandhi, from `<HI>` lines |
| dhātu | Verbal root; the verbs01 filter aligns VCP's verb entries to the known dhātu inventory |
| `#N` suffix | Homonym number on VAC headwords (`a#1`), stripped for comparison |
| hiatus changes | Gen-4 change set normalizing vowel-hiatus spellings before comparison |
| L / L-number | Cologne's stable per-entry id (`<L>` in the metaline) |

## 7. Maintainer appendix

- **What is live vs frozen:** live = `meld_regex/` (correction rounds) +
  `vac-vcp-cmp2/` (metrics) + `verbs01/` (rerunnable) + `abbrevprep/`
  (rerunnable survey) + `alternateheadword/` (analysis of record). Frozen
  archaeology = `vcpte-vcp-cmp/`, `vcpte-vac/`, `vac-vcp-cmp1/`,
  `vac-vcp-cmp1a/`, the root Excel pair, and the root-level one-off text
  harvests. Never "clean up" the frozen folders — gen-5 files begin as
  copies of gen-4 outputs, so the lineage is the provenance chain.
- **Never-touch list:** `meld_regex/vac2_split/` + `vcp2_split/` except
  through a meld correction round (§4.1); `vcpte-vac/vac_input.txt`
  (CC BY-NC-SA — the non-commercial term also caveats any downstream reuse
  of VAC-derived data); the committed gen-1–4 outputs (frozen evidence);
  `verbs01/vcp_verb_filter_{include,exclude}.txt` and
  `preverb_manualByLine.txt` (hand-curated — the filter's exact agreement
  with the dhātu list depends on them).
- **Observed defects** (found 11-07-2026 while writing this manual):
  1. `abbrevprep/redo.sh` is a copy-paste hybrid — verbs01's command block
     pasted after the abbrev0 line, which itself lacks the mode argument;
     the header comment still names `…/skd/verbs01` (itself inherited from
     the SKD repo). The readme.txt, not the redo.sh, is authoritative (§4.4).
  2. The `split_file.py` DO-NOT-REDO footgun has no mechanical guard (no
     wrapper check, chunks not read-only) — the readme is the only
     protection.
  3. `vcpte-vac/readme.org~` (an editor backup) and several `.pyc` files are
     committed.
  4. The root Excel-algo notes are cp1251 Russian (§5) — functional, but a
     trap for any tooling that assumes UTF-8 repo-wide.
- **Cross-repo contract:** corrections produced here reach the canonical
  text ONLY via the
  [csl-orig correction workflow](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md)
  (org rule: change files + queued batch PR, never a direct push — the
  `cp`-based carry script is upstream-maintainer-only). MW data consumed by
  `verbs01/` comes from the sibling
  [csl-orig/v02/mw/mw.txt](https://github.com/sanskrit-lexicon/csl-orig/blob/main/v02/mw/mw.txt).
- **Issue taxonomy:** dictionary-repo taxonomy (type / severity / milestone)
  — see [CLAUDE.md](https://github.com/sanskrit-lexicon/VCP/blob/main/CLAUDE.md);
  the comparison workflow's tracker issues are
  [#14](https://github.com/sanskrit-lexicon/VCP/issues/14),
  [#15](https://github.com/sanskrit-lexicon/VCP/issues/15),
  [#24](https://github.com/sanskrit-lexicon/VCP/issues/24).

---

_Dr. Mārcis Gasūns_
