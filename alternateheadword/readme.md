Dear all, 
https://github.com/sanskrit-lexicon/VCP/tree/master/alternateheadword is the repository where I have been playing with hw1.py of ejf - renamed as [hw1_dhaval.py](https://github.com/sanskrit-lexicon/VCP/blob/master/alternateheadword/hw1_dhaval.py).

with the [latest commit](https://github.com/sanskrit-lexicon/VCP/commit/483161702ca0611b02a8bd273252a801ce170973) incorporating [levenshtein](https://github.com/sanskrit-lexicon/VCP/blob/master/alternateheadword/levenshtein.py) logic has been added to the hw1_dhaval.py code.

Logic -
1. Separate words having brackets (for extraction of alternate headwords) - [bracketwords.txt](https://github.com/sanskrit-lexicon/VCP/blob/master/alternateheadword/bracketwords.txt)
2. Separate words having brackets in mid - [midbracket.txt](https://github.com/sanskrit-lexicon/VCP/blob/master/alternateheadword/midbracket.txt) and end - [endbracket.txt](https://github.com/sanskrit-lexicon/VCP/blob/master/alternateheadword/endbracket.txt)
3. Analyse the words and decide whether the substitution is for previous or posterior part or indeterminate.
4. Compare the suggested word from [hw1.txt](https://github.com/sanskrit-lexicon/VCP/blob/master/data/hw1.txt) (sanhw1.txt headwords only file)
5. If the suggested word is found in hw1.txt or in some of the known patterns (b,v exchange) (S-s exchange etc, then it is stored in [validated.txt](https://github.com/sanskrit-lexicon/VCP/blob/master/alternateheadword/validated.txt) for future integration in headword list.
6. If not, store in [nonvalidated.txt](https://github.com/sanskrit-lexicon/VCP/blob/master/alternateheadword/nonvalidated.txt) for manual examination.

The methods to make replacements are marked with a code '1' through "6" which can help us locate the part of hw1_dhaval.py which made these suggestions at later stage.
If there are no suggested headwords / non decision regarding the position of the string to be substituted by the bracket string, I have put "404" code. (See nonvalidated.txt)

Plan ahead -
1. validated.txt are sureshot headwords. Incorporate them. There can be a very miniscule error in this step, but worth taking risk.
2. nonvalidated.txt need manual examination. After manual corrections, they can be validated and incorporated in headword list.
3. Treatment of endbracket.txt is pending. It should be easier.

