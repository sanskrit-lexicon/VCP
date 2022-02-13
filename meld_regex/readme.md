# meld_regex/vac2 folder

Files generated from vac-vcp-cmp2/vac2.txt file taken at 13 February 2022.

`python3 split_file.py ../vac-vcp-cmp2/vac2.txt vac2_split 500 vac`

DO NOT redo this. Otherwise, it may overwrite on the files in vac2_split folder.

# meld_regex/vcp2 folder

Files generated from vac-vcp-cmp2/vcp2.txt file taken at 13 February 2022.

`python3 split_file.py ../vac-vcp-cmp2/vcp2.txt vcp2_split 500 vcp`

DO NOT redo this. Otherwise, it may overwrite on the files in vcp2_split folder.

# Methodology

1. Compare the two corresponding files in meld.
2. Make corrections on both the sides i.e. VAC and VCP.
3. `cat vac2_split/vac_* > vac3.txt`
4. `cat vcp2_split/vcp_* > vcp3.txt`
5. Compare the `vac3.txt` and `vac-vcp-cmp2/vac2.txt` file. If found suitable, copy `vac3.txt` over `vac-vcp-cmp2/vac2.txt` file.
6. Compare the `vcp3.txt` and `vac-vcp-cmp2/vcp2.txt` file. If found suitable, copy `vcp3.txt` over `vac-vcp-cmp2/vcp2.txt` file.

