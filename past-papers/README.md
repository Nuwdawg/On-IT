# Cambridge International AS Level Information Technology (9626): Past Papers, 2022 onwards

AS Level papers only: **Paper 1** (Theory) and **Paper 2** (Practical).
Papers 3 and 4 are A Level papers and aren't included.

## Folder layout

```
past-papers/<year>/<session>/
```

Sessions: `Feb-March` (m), `May-June` (s), `Oct-Nov` (w).

## File naming

`9626_<session><yy>_<type>_<component>`

| Type | Meaning |
|------|---------|
| `qp` | Question paper |
| `ms` | Mark scheme |
| `sf` | Source files for the practical paper (zip) |
| `er` | Examiner report (covers all components) |
| `gt` | Grade thresholds |

| Component | Paper |
|-----------|-------|
| `11`, `12`, `13` | Paper 1 Theory, variants 1 to 3 (Feb/March has only variant 12) |
| `02` / `2` | Paper 2 Practical (single variant) |

## Coverage

| Year | Feb-March | May-June | Oct-Nov |
|------|-----------|----------|---------|
| 2022 | ✅ | ✅ | ✅ |
| 2023 | ✅ | ✅ | ✅ |
| 2024 | ✅ | ✅ | ✅ |
| 2025 | ✅ | ✅ | ✅ |
| 2026 | ✅ | ✅ (no examiner report yet) | not sat yet |

## Note: Oct/Nov 2022 practical source files

`2022/Oct-Nov/9626_w22_sf_02.zip` is larger than GitHub's 100 MB file limit, so it's
split into parts. To rebuild the zip:

```bash
cat 9626_w22_sf_02.zip.part* > 9626_w22_sf_02.zip        # macOS / Linux
copy /b 9626_w22_sf_02.zip.part00+9626_w22_sf_02.zip.part01+9626_w22_sf_02.zip.part02 9626_w22_sf_02.zip   # Windows
```

---
These papers are © Cambridge University Press & Assessment and are here for personal revision.
