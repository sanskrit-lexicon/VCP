# In local installation, this directory is
# /c/xampp/htdocs/sanskrit-lexicon/skd/verbs01
# And csl-orig directory is
# /c/xampp/htdocs/cologne/csl-orig
# Thus csl-orig relative location relative to this directory is
CSLORIG="../../../cologne/csl-orig"
echo "abbrev0.txt"
python abbrev0.py ${CSLORIG}/v02/vcp/vcp.txt abbrev0.txt


echo "remake vcp_verb_filter"
python vcp_verb_filter.py temp_vcp.txt vcp_verb_filter_exclude.txt vcp_verb_filter_include.txt vcp_verb_filter.txt
echo "remake vcp_verb_filter_map"
python vcp_verb_filter_map.py vcp_verb_filter.txt mwverbs1.txt vcp_verb_filter_map.txt
echo "remake vcp_preverb1.txt"
python preverb1.py slp1 temp_vcp.txt vcp_verb_filter_map.txt mwverbs1.txt vcp_preverb1.txt
echo "remake vcp_verb1.txt"
python verb1.py slp1 temp_vcp.txt vcp_preverb1.txt vcp_verb1.txt
echo "remake vcp_verb1_deva.txt"
python verb1.py deva temp_vcp.txt vcp_preverb1.txt vcp_verb1_deva.txt

echo "REDO.SH done"
echo "now manually copy to sanskrit-lexicon/vcp/verbs01/ using"
echo "sh redo_copy.sh"
