
This work was originally done in a temporary subdirectory of
csl-orig/v02/vcp.   Thus, the relative paths (e.g. ../../mw/mw.txt) 
would need modification.

* mwverbs
python mwverb.py mw ../../mw/mw.txt mwverbs.txt
#copy from v02/mw/temp_verbs
#cp ../../mw/temp_verbs/verb.txt mwverbs.txt
each line has 5 fields, colon delimited:
 k1
 L
 verb category: genuinroot, root, pre,gati,nom
 cps:  classes and/or padas. comma-separated string
 parse:  for pre and gati,  shows x+y+z  parsing prefixes and root

* mwverbs1.txt
python mwverbs1.py mwverbs.txt mwverbs1.txt
Merge records with same key (headword)
Also  use 'verb' for categories root, genuineroot, nom
and 'preverb' for categories pre, gati.
Format:
 5 fields, ':' separated
 1. mw headword
 2. MW Lnums, '&' separated
 3. category (verb or preverb)
 4. class-pada list, ',' separated
 5. parse. Empty for 'verb' category. For preverb category U1+U2+...+root

* 02-23-2020  vcp_verb_filter.txt
python vcp_verb_filter.py ../vcp.txt vcp_verb_filter_exclude.txt vcp_verb_filter_include.txt vcp_verb_filter.txt

The exclude and include files are made so that the verbs in vcp_verb_filter
exactly agree with VCP-dhatus.txt.


* vcp_verb_filter_map
python vcp_verb_filter_map.py vcp_verb_filter.txt mwverbs1.txt vcp_verb_filter_map.txt

Get correspondences between vcp verb spellings and
 - vcp verb spellings
 - mw verb spellings

2243 verbs mapped to MW verbs
1985  of the mapped mwspellings differ from the vcp spellings
34 verbs are unmapped


* temp_vcp.txt
There are several (~ 40) upasargas which are, in vcp.txt, indicated by a 
different pattern.
Example: <HI>parA--nirAkAraRe   non-standard parA
instead: <HI>parA + nirAkAraRe  standard parA
It is convenient to recode these lines of vcp.txt so that preverb1 and
other programs required to identify and parse preverbs only need to deal
with the more common '+' text.
We can make an alternate version of the digitization (temp_vcp.txt) that
converts the non-standard forms to the standard form.
We could do this in vcp.txt itself; these would be print changes.
Not sure if we should change vcp.txt.
Currently, we are just making a temporary variant version, temp_vcp.txt.
and using this temporary version in preverb1 and verb1.
First, we use a program to construct change transactions,
then apply the change transactions.

python analyze_preverb.py ../vcp.txt preverb_manualByLine.txt
 (48 change transactions)
python updateByLine.py ../vcp.txt preverb_manualByLine.txt temp_vcp.txt

* preverb1.txt
python preverb1.py slp1 temp_vcp.txt vcp_verb_filter_map.txt mwverbs1.txt vcp_preverb1.txt

For each of the entries of vcp_verb_filter_map.txt, the program analyzes the
text of VCP looking for upasargas.  An upsarga is identifed by the pattern
(in Python syntax): 

`re.search(r'^<HI>([a-zA-Z +]+) [+] ',line)`.
For example : `<HI>upa + A + AramBe upAkaroti upAkftya “SrAvaRyAM prozWa`
 is parsed as 'upa + A', and then (by sandhi) converted to prefix 'upA'.
The file 'vcp_upasarga_parse.txt' has all the cases, with frequency counts.
There are 102 different patterns, and 700 (non-distinct) patterns found;
and these occur within 96 different root entries.

For each upasarga, an attempt is made to match the prefixed verb to a
known MW prefixed verb.  

*  vcp_verb1.txt and vcp_verb1_deva.txt
python verb1.py slp1 temp_vcp.txt vcp_preverb1.txt vcp_verb1.txt
python verb1.py deva temp_vcp.txt vcp_preverb1.txt vcp_verb1_deva.txt

vcp_verb1.txt  provides the text content for each of the verbs mentioned
in vcp_preverb1.txt. 
The upasargas are indicated by lines starting with '*<HI>'.

vcp_verb1_deva.txt is the same, except that the Sanskrit text is rendered in Devanagari,
rather than the slp1 of vcp_verb1.txt.
