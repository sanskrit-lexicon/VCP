
A log of the changes to vac2.txt and vcp2.txt.
The initialization of these files is described in readme.txt.
214654 lines are nearly the same (out of 410046 lines)

1. vac2: replace long lines and generate picturedata.txt
  python vac00a.py vac2.txt temp_vcp1a.txt temp_vac00a.txt picturedata.txt
  mv temp_vac00a.txt vac2.txt

2. vcp: ai/au hiatus changes
  changes_vcp_1_hiatus.txt has the changes made to vcp.txt
  python updateByLine.py vcp.txt changes_vcp_1_hiatus.txt temp_vcp.txt
  mv temp_vcp.txt vcp.txt

2a. changes_vac_01.txt  (31 changes)
  These noticed while developing changes_vcp_1_hiatus.txt.
  python updateByLine.py vac2.txt changes_vac_01.txt temp_vac2.txt
  mv temp_vac2.txt vac2.txt
  # now recompute
  sh redo_vcp2.sh
214980 records are nearly the same.

