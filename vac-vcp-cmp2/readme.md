# readme.org for vac-vcp-cmp2
Begun Jan 15, 2021
Dr. Dhaval Patel
This continues the work begun in vac-vcp-cmp1 folder.

# Requirement

`pip install simplediff`

# Usage 

`python3 len2.py vcp1.txt vac1.txt hwdiff.tsv len2.tsv`


# vac1.txt

For the Tirupati edition, this work uses the vac.txt (Scharf edition of Tirupati edition of Vacaspatyam):  see vcpte-pms folder.

Here, 'vac' refers to this Scharf version of Tirupati edition of Vacaspatyam.

#  vcp1.txt

'vcp' refers to the Cologne edition of Vacaspatyam.

This begins as the copy of Cologne edition of Vacaspatyam, as accessed from https://github.com/sanskrit-lexicon/csl-orig/blob/master/v02/vcp/vcp.txt on 15 Jan 2021.
It is the Cologne edition of Vacaspatyam, in slp1 transliteration and with utf-8 encoding.

# len2.py

Usage - `python3 len2.py vcp1.txt vac1.txt hwdiff.tsv len2.tsv`


Takes vcp1.txt and vac1.txt as input and calculates the differences and stores them in two files. 

There are certain assumptions in the process.

1. All non alphabet items `[^a-zA-Z]` are ignored for comparing.
2. All XML like tags are removed. `<[^>]*>`
3. Trailing numbers are removed from headwords in vac1.txt (`aMSa#1 -> aMSa`)
4. Only one parse is retained from headword from vac1.txt (`aMsa(se)BAra -> aMsaBAra`)
5. vac1.txt usually has one headword per line. If there are more than one entries, they are clubbed together in vac1.txt. vcp1.txt treats them separately. To make them at par, the following method is followed. All the entries for a particular headword are concatenated. e.g. vac1.txt has `a#1`  and `a#2` headwords. If their entries are `e1` and `e2`, the text which is generated for headword `a` is `e1 e2`. Similarly for vcp1.txt. 

The contents of output files hwdiff.tsv and len2.tsv are explained later.

# hwdiff.tsv

Shows the headwords for which there are unequal numbers of entries in VAC and VCP, in the following tab separated format

`headword	countInVcp	countInVac`

e.g. 
```
AgrahAyARika	0	1
AgrahAyaRika	2	1
```
This would mean that there are 0 occurrences of AgrahAyARika in VCP, and 1 occurrence in VAC. 
Similarly, for AgrahAyaRika, there are 2 occurrences in VCP, and 1 in VAC.
(In the present case, AgrahAyaRika is the correct word. AgrahAyARika in VAC is an error, which needs to be corrected.)

# len2.tsv

Tab separated file with the following fields
`headword	vacEntryWithDiff	vcpEntry`

When there is no such headword in VAC or VCP, the corresponding data is blank.
When there are such headwords in both VAC and VCP, the VAC entry is shown with `<ins>` and `<del>` tags, which would make it identical to VCP entry. 
This diff highlighting is done for easier location of error in large entries.

# tsv_to_html.py

Generates HTML table from tsv files.

Usage - `tsv_to_html.py tsvfile htmlfile`
e.g.
`tsv_to_html.py hwdiff.tsv hwdiff.html`
or
`tsv_to_html.py len2.tsv len2.html`

# hwdiff.html

HTML file with links to Text and PDF from Cologne dictionaries, in the following format, for checking.

`headwordWitTextLink	headwordWithPDFLink	countInVcp	countInVac`

# len2.html

HTML file with links to Text and PDF from Cologne dictionaries, in the following format, for checking.

`headwordWithTextLink	headwordWithPDFLink	vacEntryWithDiff	vcpEntry`

# What next

1. Open hwdiff.html and inspect the headwords, by clicking on the links. 
2. Open vac1.txt and vcp1.txt.
3. Make necessary corrections to vac1.txt and vcp1.txt.
4. Rerun the program by `bash redo.sh`.
5. This will regenerate the output. This would remove the issues which have already been corrected.
6. Keep on the process, till there are no differences between two digitizations, or they are explainable.

Note - We should not be hesitant to make changes to vac1.txt or vcp1.txt files in vac-vcp-cmp2 repository. The reason is that their base versions are available at https://github.com/sanskrit-lexicon/VCP/blob/master/vac-vcp-cmp1/vcp1.txt and https://github.com/sanskrit-lexicon/csl-orig/blob/master/v02/vcp/vcp.txt. They are not affected by our changes at vac-vcp-cmp2 repository.


