# AS Level IT (9626) Paper 1: Topical Past Papers

Every Paper 1 (Theory) question from Feb/March 2022 to May/June 2026, sorted by
syllabus topic. Each topic has one PDF:

| PDF | Questions |
|-----|-----------|
| `01 - Data processing and information.pdf` | 87 |
| `02 - Hardware and software.pdf` | 59 |
| `03 - Monitoring and control.pdf` | 35 |
| `04 - Algorithms and flowcharts.pdf` | 29 |
| `05 - eSecurity.pdf` | 30 |
| `06 - The digital divide.pdf` | 17 |
| `07 - Expert systems.pdf` | 20 |
| `08 - Spreadsheets.pdf` | 11 |
| `09 - Modelling.pdf` | 17 |
| `10 - Database and file concepts.pdf` | 35 |
| `11 - Video and audio editing.pdf` | 14 |

## How each PDF is laid out

- **Questions** come first, oldest paper first. Each one is cut straight from
  the original paper, answer lines included, and labelled with its source,
  e.g. *9626/12 Feb/March 2022 · Question 7*.
- **Mark schemes** follow in the same order.
- Click **Mark scheme** next to a question to jump to its answers, and
  **Back to question** to return. The bookmarks panel lists every question.

## Notes

- Topic names follow the 2025–2027 syllabus. Cambridge says its content is
  largely the same as the 2022–2024 syllabus.
- A question that covers more than one topic is in each of those PDFs. For
  example, a pseudocode question about a greenhouse is in both *Monitoring and
  control* and *Algorithms and flowcharts*. That's why the counts above add up
  to more than the 338 questions.
- Oct/Nov 2025 papers 9626/11 and 9626/13 have the same questions, so they
  appear once, labelled with both codes.
- Topics were assigned by reading each question. If you'd file a question
  differently, change its topic numbers in `tools/question_topics.json` and
  rebuild.

## Rebuilding

```bash
pip install pymupdf
python tools/build_topical.py check   # every paper splits cleanly into questions
python tools/build_topical.py build   # rewrites the PDFs in this folder
```

---
Source: Cambridge International 9626 past papers © UCLES / Cambridge University
Press & Assessment, for personal revision.
