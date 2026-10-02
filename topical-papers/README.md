# AS Level IT (9626) Paper 1: High-Signal Topical Questions

| PDF | What's in it |
|-----|--------------|
| `AS Level IT 9626 - Paper 1 high-signal questions.pdf` | 110 questions: 10 for each of the 11 AS Level topics, without answer space |
| `AS Level IT 9626 - Paper 1 high-signal mark schemes.pdf` | The mark schemes for those questions, in the same order |

Topics: 1 Data processing and information · 2 Hardware and software ·
3 Monitoring and control · 4 Algorithms and flowcharts · 5 eSecurity ·
6 The digital divide · 7 Expert systems · 8 Spreadsheets · 9 Modelling ·
10 Database and file concepts · 11 Video and audio editing

## How the questions were picked

Each topic's 10 come from all 338 Paper 1 questions from Feb/March 2022 to
May/June 2026. Together they cover the points that topic tests most often,
favouring longer (6–8 mark) and more recent questions. Repeats are left out, and
no question appears under two topics. Within a topic they follow the syllabus
order.

The shortlist is `tools/high_signal.json`. To swap a question, edit it and rebuild.

## Layout

- The contents page links to each topic.
- Questions are numbered 1.1 to 11.10 and labelled with the paper they came
  from, e.g. *1.2 9626/12 May/June 2024 · Question 7*. The mark schemes use the
  same numbers.
- The questions PDF leaves out the blank answer lines and empty answer boxes.
  Each part keeps its marks, e.g. **[4]**, and labels such as "Humidity" or
  "Way 1". Tables, diagrams and code to complete are kept. Where an algorithm
  has missing lines, one dotted line marks each gap.
- Long questions and mark schemes run on to the next page, split between lines.
- The bookmarks panel lists every question.

## Notes

- Topic names follow the 2025–2027 syllabus. Cambridge says its content is
  largely the same as the 2022–2024 syllabus.
- Oct/Nov 2025 papers 9626/11 and 9626/13 have the same questions, so those
  questions are labelled with both codes.
- `tools/question_topics.json` gives the topics of every question, not just the
  shortlisted ones.

## Rebuilding

```bash
pip install pymupdf
python tools/build_topical.py check   # every paper splits cleanly into questions
python tools/build_topical.py build   # rewrites both PDFs in this folder
```

---
Source: Cambridge International 9626 past papers © UCLES / Cambridge University
Press & Assessment, for personal revision.
