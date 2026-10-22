# 9702 Paper 4 — topical papers (7 hardest questions per topic)

One PDF per A Level topic of the 2025–2027 syllabus (topics 12–25). Each PDF
holds the seven hardest past-paper questions on that topic, taken from every
Paper 4 in `physics-9702-paper-4/` (Feb/March, May/June and Oct/Nov, 2020–2026,
all variants).

Each PDF is laid out as:

1. **Contents page**: the seven questions, hardest first, each with its source
   paper, page number and the examiner-report remark that marked it as hard.
2. **Questions**: cropped straight from the original question papers, with the
   original diagrams, answer lines and `[Total: n]`.
3. **Mark schemes**: the matching mark-scheme rows for every question, in the
   same order.

| Topic | Questions (hardest first) |
|---|---|
| 12 Motion in a circle | O/N/21/42 Q1, M/J/23/41 Q2, O/N/25/42 Q1, O/N/23/42 Q1, F/M/25/42 Q1, O/N/25/41 Q1, M/J/26/42 Q1 |
| 13 Gravitational fields | F/M/21/42 Q1, O/N/23/42 Q2, O/N/22/42 Q1, O/N/21/41 Q2, F/M/20/42 Q1, F/M/22/42 Q1, M/J/22/41 Q1 |
| 14 Temperature | M/J/25/41 Q3, F/M/25/42 Q3, O/N/24/42 Q3, M/J/23/41 Q3, O/N/22/41 Q2, O/N/25/42 Q3, F/M/26/42 Q3 |
| 15 Ideal gases | O/N/21/41 Q3, M/J/21/41 Q2, O/N/22/42 Q3, O/N/24/42 Q4, F/M/23/42 Q2, F/M/21/42 Q2, M/J/21/42 Q2 |
| 16 Thermodynamics | F/M/24/42 Q2, M/J/23/42 Q3, M/J/23/41 Q4, O/N/25/42 Q4, M/J/25/41 Q4, O/N/23/41 Q2, O/N/20/41 Q2 |
| 17 Oscillations | F/M/22/42 Q3, M/J/21/41 Q3, M/J/22/41 Q4, O/N/21/41 Q4, O/N/21/42 Q4, M/J/21/42 Q3, O/N/25/44 Q4 |
| 18 Electric fields | O/N/20/41 Q5, O/N/22/41 Q4, O/N/22/42 Q5, O/N/23/41 Q5, M/J/22/41 Q2, F/M/23/42 Q4, O/N/25/44 Q5 |
| 19 Capacitance | F/M/23/42 Q5, O/N/21/41 Q6, F/M/22/42 Q5, O/N/21/42 Q6, O/N/22/42 Q6, M/J/21/41 Q7, M/J/23/42 Q5 |
| 20 Magnetic fields | M/J/25/44 Q6, M/J/25/44 Q7, M/J/22/42 Q6, M/J/21/41 Q10, M/J/22/42 Q7, F/M/24/42 Q6, O/N/24/42 Q1 |
| 21 Alternating currents | O/N/23/41 Q7, O/N/22/41 Q7, M/J/23/42 Q7, M/J/25/41 Q6, O/N/25/44 Q6, M/J/24/41 Q7, M/J/22/41 Q5 |
| 22 Quantum physics | F/M/22/42 Q8, F/M/23/42 Q7, O/N/22/41 Q8, O/N/23/41 Q8, F/M/25/42 Q8, O/N/20/42 Q11, F/M/20/42 Q10 |
| 23 Nuclear physics | M/J/22/41 Q8, O/N/20/42 Q12, M/J/23/41 Q9, M/J/23/42 Q9, O/N/21/42 Q12, O/N/22/41 Q10, F/M/24/42 Q8 |
| 24 Medical physics | O/N/20/42 Q7, M/J/23/42 Q10, F/M/21/42 Q11, M/J/22/41 Q9, O/N/25/42 Q10, O/N/25/44 Q8, F/M/20/42 Q4 |
| 25 Astronomy and cosmology | M/J/22/41 Q10, O/N/25/41 Q9, F/M/24/42 Q10, F/M/22/42 Q12, O/N/23/42 Q10, M/J/24/42 Q8, M/J/22/42 Q9 |

## How the questions were chosen

- Every question in all 49 papers was tagged with the syllabus topics it
  examines. Questions on content that has since left the syllabus (op-amps,
  sensors, communication/AM, optic fibres, MRI, transformers, band theory,
  decibels and so on, mostly in 2020–2021 papers) were excluded.
- Each question was scored from its examiner report comments: phrases such as
  "very few candidates", "only the strongest", "rarely seen", "challenging" and
  common misconceptions count towards difficulty, while "well answered" and
  "most candidates" count against it. The shortlist was then read through by
  hand and the seven hardest kept, preferring questions that test the core of
  the topic rather than a single hard mark buried in another topic's question.
- Variant 43 is identical to variant 41 in every series, so each question
  appears once only. In Oct/Nov the /41 report says "too few candidates" and
  the comments for the identical /43 question are used instead.
- June 2020 (series cancelled) and June 2026 have no examiner reports. Where a
  report gave no usable evidence, judgement was used and the contents page says
  so.

## Rebuilding

```
python3 tools/physics_topical.py split   # split papers, mark schemes and reports into questions (cached)
python3 tools/physics_topical.py dump 19 # list every question tagged with a topic, with report comments
python3 tools/physics_topical.py build   # write the 14 PDFs into this folder
```

The choices and topic tags live in `tools/physics_topical.json`. Requires
`pymupdf` and `reportlab`, plus the fonts fetched by
`tools/physics_papers/get_arial.sh`.
