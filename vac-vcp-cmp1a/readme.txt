readme.txt for vac-vcp-cmp1a
Begun Mar 14, 2021
Builds on vac-vcp-cmp1, using current 2021 vcp.txt 
 from csl-orig/

This continues the work begun in vcpte-vcp-cmp1 folder.

Here, 'vac' refers to this Scharf version of Tirupati edition of Vacaspatyam.
Also, 'vcp' refers to the Cologne edition of Vacaspatyam.

vcp.txt starts as a copy from csl-orig/v02/vcp/vcp.txt at 03-15-2021

vac2.txt starts as a copy of vac-vcp-cmp1/vac2.txt

vcp.txt and vac2.txt are not directly comparable, since vcp.txt has metaline data.
Thus we compute a form vcp2.txt from vcp.txt so that
vcp2.txt and vac2.txt are comparable.

This is done by redo_vcp2.sh script, in two steps:
1) compute an intermediate form temp_vcp1.txt
   At the same time, compute a temporary mapping file (vcp2_map.txt) of
   corresponding line numbers from temp_vcp1.txt to vcp.txt
# removes the '<L>, '<LEND>', lines, AND
# places [Pagexxx] on previous line
changes x¦ to <HI>{@x@}¦
   
python make_vcp1.py vcp.txt temp_vcp1.txt vcp2_map.txt
2) Then compute vcp2.txt; at the same time, do a comparison of
  each line of vac2.txt and vcp2.txt to get a difference statistic for
  each line.
python make_vcp2.py vac2.txt temp_vcp1.txt vcp2.txt

Our procedure now is to revise, by various means, vac2.txt and vcp.txt
and then to recompute vcp2.txt, gathering statistics on differences.

See readme_changes.txt for details of the progression of changes
to va
* temp_vcp1a.txt and temp_vcp2a_map.txt
# make temp_vcp1a.txt in same format as ../vac-vcp-cmp1/vcp1.txt

python make_vcp1a.py temp_vcp.txt temp_vcp1a.txt temp_vcp2a_map.txt

* vac2a.txt
python make_vac2a.py ../vac-vcp-cmp1/vac2.txt temp_vcp1a.txt vac2a.txt vac2a_picturedata.txt

* vcp2a.txt
python make_vcp2a.py vac2a.txt temp_vcp1a.txt vcp2a.txt

vcp2a.txt adds line number and code (vcp) and a 'diffcount' to lines of
temp_vcp1a.txt.

Example line 4:
../vac_vcp_cmp1/vac2.txt
000004:2:  te: vA+qa. </vkr><reN1> vizRO <q>akAro vizRuruddizwa ukArastu maheSvaraH

temp_vcp1a.txt:
<>vA qa . vizRO “akArovizRuruddizwOkArastu maheSvaraH .

vcp2a.txt:
000004:2: vcp: <>vA qa . vizRO “akArovizRuruddizwOkArastu maheSvaraH .


The diff number  in vcp2a.txt in this line is '2'.
This is the edit-distance between the 'te' line and the 'vcp' line,
 after adjustment (various removals of 'extraneous' information).

te-adj : vAqavizROakArovizRuruddizwaukArastumaheSvaraH
vcp-adj: vAqavizROakArovizRuruddizwOkArastumaheSvaraH

edit-distance = 2


python make_hiatus_changes.py vac2a.txt vcp2a.txt temp_vcp2a_map.txt temp_make_hiatus_changes.txt

cp temp_make_hiatus_changes.txt changes_vcp_1_hiatus.txt
This is edited manually.  It contains changes to be applied to vcp.txt
python updateByLine.py temp_vcp.txt changes_vcp_1_hiatus.txt temp_vcp_1.txt

mv temp_vcp.txt tempprev_vcp.txt
mv temp_vcp_1.txt temp_vcp.txt
