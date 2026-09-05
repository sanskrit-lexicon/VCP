_Created: 22-05-2026 · Last updated: 05-09-2026_

### Location

Counterpart of https://github.com/sanskrit-lexicon/PWG/issues/175 (PWG) and https://github.com/sanskrit-lexicon/PWK/issues/113 (PWK) for `vcp.txt`.

I ran the same two-job recipe over `csl-orig/v02/vcp/vcp.txt`: auto-fix the few things with a single safe resolution; audit everything else with line refs. Added `08_markup_fix.py` plus outputs to a new `vcpissues/markup_fix/` folder on the branch `markup-fix-audit`.

@funderburkjim @Andhrabharati — please review the findings listed below.

## Markup fixer + audit for `vcp.txt`

### What it auto-fixes

_(no paired tags — fixer retained as a re-runnable baseline)_

Whitespace trimming applies to all 0 paired tag(s) in `vcp.txt`: _(no paired tags)_. The original file is never modified — output goes to `vcp_fixed.txt`, with the full diff in `markup_fix_changes.txt` (updateByLine format). **Output is byte-identical to source** (no auto-fixes triggered).

### Closing-tag inventory in current `vcp.txt`

_(none)_ — vcp.txt/ccs.txt uses only structural record-delimiter tags.

### What it found in current `vcp.txt`

- 0 paired tags — vcp.txt uses no inline paired markup tags.
- 0 auto-fixes — byte-identical to source.
- 48 `{{old → new || …}}` correction records present.

### Usage

```
cd vcpissues/markup_fix
python 08_markup_fix.py                        # uses csl-orig/v02/vcp/vcp.txt by default
python 08_markup_fix.py IN.txt OUT.txt         # custom paths
```

Outputs: `vcp_fixed.txt`, `markup_fix_changes.txt`, `markup_audit.txt`.

### Summary

No paired tags; fixer retained as a re-runnable baseline.

### Severity

`minor`

_Dr. Mārcis Gasūns_
