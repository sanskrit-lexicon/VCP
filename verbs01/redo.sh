echo "remake mwverbs"
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
echo "remake mwverbs1"
python mwverbs1.py mwverbs.txt mwverbs1.txt
echo "remake vcp_verb_filter"
python vcp_verb_filter.py ../vcp.txt vcp_verb_filter_exclude.txt vcp_verb_filter_include.txt vcp_verb_filter.txt
echo "remake vcp_verb_filter_map"
python vcp_verb_filter_map.py vcp_verb_filter.txt mwverbs1.txt vcp_verb_filter_map.txt
echo "remake vcp_preverb1.txt"
python preverb1.py slp1 temp_vcp.txt vcp_verb_filter_map.txt mwverbs1.txt vcp_preverb1.txt
echo "remake vcp_verb1.txt"
python verb1.py slp1 temp_vcp.txt vcp_preverb1.txt vcp_verb1.txt
echo "remake vcp_verb1_deva.txt"
python verb1.py deva temp_vcp.txt vcp_preverb1.txt vcp_verb1_deva.txt
