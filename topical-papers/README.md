# AS Level IT (9626) Paper 1: Topical Past Papers

`AS Level IT 9626 - Paper 1 topical past papers.pdf` holds every Paper 1
(Theory) question from Feb/March 2022 to May/June 2026, sorted by syllabus topic:

| Topic | Questions |
|-------|-----------|
| 1 Data processing and information | 87 |
| 2 Hardware and software | 59 |
| 3 Monitoring and control | 35 |
| 4 Algorithms and flowcharts | 29 |
| 5 eSecurity | 30 |
| 6 The digital divide | 17 |
| 7 Expert systems | 20 |
| 8 Spreadsheets | 11 |
| 9 Modelling | 17 |
| 10 Database and file concepts | 35 |
| 11 Video and audio editing | 14 |

## How the PDF is laid out

- The **contents page** links to the start of each topic's questions and mark
  schemes.
- Each topic has its **questions** first, oldest paper first. Each one is cut
  straight from the original paper, answer lines included, and labelled with
  its source, e.g. *9626/12 Feb/March 2022 · Question 7*. The topic's **mark
  schemes** follow in the same order.
- Click **Mark scheme** next to a question to jump to its answers, and
  **Back to question** to return. The bookmarks panel lists every question.

## Notes

- Topic names follow the 2025–2027 syllabus. Cambridge says its content is
  largely the same as the 2022–2024 syllabus.
- A question that covers more than one topic appears under each of them. For
  example, a pseudocode question about a greenhouse is under both *Monitoring and
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
python tools/build_topical.py build   # rewrites the PDF in this folder
```

---
Source: Cambridge International 9626 past papers © UCLES / Cambridge University
Press & Assessment, for personal revision.
