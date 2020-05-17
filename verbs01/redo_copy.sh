DIR="/c/xampp/htdocs/sanskrit-lexicon/VCP/verbs01"
for FILE in mwverbs.txt mwverbs1.txt \
    vcp_verb_filter_include.txt vcp_verb_filter_exclude.txt \
    vcp_verb_filter.txt vcp_verb_filter_map.txt \
    vcp_preverb1.txt \
    vcp_verb1.txt vcp_verb1_deva.txt\
    vcp_verb_filter.py redo.sh redo_copy.sh
do
echo "cp $FILE $DIR/$FILE"
cp $FILE $DIR/$FILE
done
