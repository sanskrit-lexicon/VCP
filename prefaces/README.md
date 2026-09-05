_Created: 22-06-2026 · Last updated: 05-09-2026_

# VCP front matter (*Vācaspatyam*) — OCR + translations

Faithful OCR of the **front matter** (title pages, publisher's note, dedication, preface, contents) of Tāranātha Tarkavācaspati's ***Vācaspatyam***, from the Cologne csldoc scans, with English and Russian translations and consolidated single-file editions.

- **Dictionary**: *Vācaspatyam* (बृहत् संस्कृताभिधानम्), a comprehensive indigenous Sanskrit→Sanskrit encyclopedic lexicon.
- **Author / compiler**: Śrī Tāranātha Tarkavācaspati Bhaṭṭācārya, Professor of Grammar and Philosophy, Govt. Sanskrit College, Calcutta.
- **Edition scanned**: Chowkhamba Sanskrit Series, Work No. 94, Vol. I — Varanasi, 1962 (Vikrama Saṃvat 2018); a reprint of the original (1873–1884).
- **Source scans**: [Cologne csldoc front-matter index](https://sanskrit-lexicon.uni-koeln.de/scans/csldev/csldoc/build/dictionaries/prefaces/vcppref.html).

This front matter is **mixed-language**: the title page and publisher page are in **Sanskrit / Devanāgarī** (`source_lang: sa`), while the second title page, publisher's note, dedication, preface, and contents are in **English** (`source_lang: en`). The digitizer running-header and footer stamps were omitted; library shelfmarks / accession stamps are noted in HTML comments but not transcribed as text.

## File conventions

| Suffix | Meaning |
|---|---|
| `vcpprefNN.md` | Source-language transcription (Sanskrit or English, per page) |
| `vcpprefNN.en.md` | English. For Sanskrit pages this is a translation; for English pages it reproduces the English source verbatim. |
| `vcpprefNN.ru.md` | Russian translation |

Each file opens with a YAML block (`source_scan`, `source_page`, `volume`, `source_url`, and `language`/`source_lang`).

## Consolidated editions

| File | Description |
|---|---|
| [`vcppref_all.sa.md`](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref_all.sa.md) | All pages, source language (Sanskrit + English) |
| [`vcppref_all.en.md`](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref_all.en.md) | All pages, English |
| [`vcppref_all.ru.md`](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref_all.ru.md) | All pages, Russian (Русский) |
| [`build_combined.py`](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/build_combined.py) | Reproducible builder — `DICT=vcp python build_combined.py` |

## Contents

| # | Section | Vol. | Lang | Source | en | ru |
|---|---|---|---|---|---|---|
| 01 | Title Page | 1 | sa | [.md](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref01.md) | [.en](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref01.en.md) | [.ru](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref01.ru.md) |
| 02 | Publisher | 1 | sa | [.md](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref02.md) | [.en](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref02.en.md) | [.ru](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref02.ru.md) |
| 03 | Title Page (English) | 1 | en | [.md](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref03.md) | [.en](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref03.en.md) | [.ru](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref03.ru.md) |
| 04 | Publisher's Note | 1 | en | [.md](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref04.md) | [.en](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref04.en.md) | [.ru](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref04.ru.md) |
| 05 | Dedication | 1 | en | [.md](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref05.md) | [.en](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref05.en.md) | [.ru](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref05.ru.md) |
| 06 | Preface | 1 | en | [.md](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref06.md) | [.en](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref06.en.md) | [.ru](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref06.ru.md) |
| 07 | Contents | 1 | en | [.md](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref07.md) | [.en](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref07.en.md) | [.ru](https://github.com/sanskrit-lexicon/VCP/blob/main/prefaces/vcppref07.ru.md) |

## Signatures & dates found

- **Title pages**: Vikrama Saṃvat 2018 / A.D. 1962 (Chowkhamba reprint).
- **Dedication**: dedicated to H.H. Sree Maharajah Meerza Ananda Gazapatti Raj of Vizianagaram, signed *Taranatha Tarkavachaspati, the Author*.
- **Preface**: signed **H. Woodrow, M.A.**, Inspector of Schools, Lower Provinces of Bengal; cites Govt. of Bengal sanction letters No. 507 (26 January 1866) and No. 3480 (12 December 1870), and the Panini grammar edition of 1863 (recommended by E. B. Cowell).

19th-century English spellings in the source (*shewn*, *ancesters*, *Kookery*) are preserved verbatim. Devanāgarī and Sanskrit names are kept verbatim; Russian translations use Cyrillic personal names.

_Dr. Mārcis Gasūns_
