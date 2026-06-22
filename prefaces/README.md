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
| [`vcppref_all.sa.md`](vcppref_all.sa.md) | All pages, source language (Sanskrit + English) |
| [`vcppref_all.en.md`](vcppref_all.en.md) | All pages, English |
| [`vcppref_all.ru.md`](vcppref_all.ru.md) | All pages, Russian (Русский) |
| [`build_combined.py`](build_combined.py) | Reproducible builder — `DICT=vcp python build_combined.py` |

## Contents

| # | Section | Vol. | Lang | Source | en | ru |
|---|---|---|---|---|---|---|
| 01 | Title Page | 1 | sa | [.md](vcppref01.md) | [.en](vcppref01.en.md) | [.ru](vcppref01.ru.md) |
| 02 | Publisher | 1 | sa | [.md](vcppref02.md) | [.en](vcppref02.en.md) | [.ru](vcppref02.ru.md) |
| 03 | Title Page (English) | 1 | en | [.md](vcppref03.md) | [.en](vcppref03.en.md) | [.ru](vcppref03.ru.md) |
| 04 | Publisher's Note | 1 | en | [.md](vcppref04.md) | [.en](vcppref04.en.md) | [.ru](vcppref04.ru.md) |
| 05 | Dedication | 1 | en | [.md](vcppref05.md) | [.en](vcppref05.en.md) | [.ru](vcppref05.ru.md) |
| 06 | Preface | 1 | en | [.md](vcppref06.md) | [.en](vcppref06.en.md) | [.ru](vcppref06.ru.md) |
| 07 | Contents | 1 | en | [.md](vcppref07.md) | [.en](vcppref07.en.md) | [.ru](vcppref07.ru.md) |

## Signatures & dates found

- **Title pages**: Vikrama Saṃvat 2018 / A.D. 1962 (Chowkhamba reprint).
- **Dedication**: dedicated to H.H. Sree Maharajah Meerza Ananda Gazapatti Raj of Vizianagaram, signed *Taranatha Tarkavachaspati, the Author*.
- **Preface**: signed **H. Woodrow, M.A.**, Inspector of Schools, Lower Provinces of Bengal; cites Govt. of Bengal sanction letters No. 507 (26 January 1866) and No. 3480 (12 December 1870), and the Panini grammar edition of 1863 (recommended by E. B. Cowell).

19th-century English spellings in the source (*shewn*, *ancesters*, *Kookery*) are preserved verbatim. Devanāgarī and Sanskrit names are kept verbatim; Russian translations use Cyrillic personal names.
