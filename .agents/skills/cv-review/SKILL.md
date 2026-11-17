---
name: cv-review
description: >-
  Evaluate, score (0-100 across section sub-metrics), audit for ATS/OCR/layout traps,
  match Top 5 job positions, and optionally apply safe edits to resumes and CVs from PDFs,
  images, text/LaTeX, Google Docs, or Canva designs. Use whenever a user asks to review,
  score, evaluate, audit, compare, improve, or rewrite a CV or resume, check photo or
  margin alignment, or recommend matching job roles.
---

# CV Review & ATS Auditor

Perform rigorous, evidence-based CV evaluations across **content**, **visual geometry**, and **real ATS/OCR parseability**, followed by concrete **Before → After** improvements and **Top 5 Job Positions** grounded strictly in observed evidence.

---

## Core Rules (Non-Negotiable)

1. **Never fabricate metrics or claims.** When an achievement needs numbers (latency, FPS, %, team size, GPA), use bracketed placeholders like `[X ms]` or `[Y teams]` until the user supplies real data.
2. **Ground every deduction in direct observation.** Always inspect both the **visual rendering** (screenshot / PNG / thumbnail) and the **extracted text/structure** (OCR / PDF stream / Canva element positions).
3. **Never inflate scores.** Separate raw candidate potential from document execution so high-potential candidates with structural/ATS issues see exactly why points were lost and how fast they can recover them.
4. **Read-only by default; approval-gated for edits.** Never mutate a Canva design or local file without explicit user request, and never commit Canva edits without showing a preview thumbnail and obtaining explicit confirmation.
5. **Match user language for feedback; preserve CV language for copy.** Answer in the user's language (e.g., Portuguese or English), while providing copy-ready CV rewrites in the CV's own language.

---

## Workflow

### Step 1: Ingest the CV (Visual + Structural)

Identify the input format and gather both visual and structural data before scoring:

- **PDF file (local path or attached PDF):**
  - Visually inspect every page (if rendered screenshots/OCR are provided, examine both side-by-side!).
  - When a local `.pdf` path is accessible and Python 3 is available, run the zero-dependency forensic auditor located inside this skill folder:
    ```bash
    python <skill_dir>/scripts/audit_pdf_ats.py "<path/to/cv.pdf>"
    ```
  - Always compare the **visual image** against the **extracted OCR/plain text** to catch hidden white-font text, broken icon-only links, letter-spaced headings (`E X P E R I E N C E`), hyphenation splits (`Pre-cision`), and A3 vs A4 page sizes.
- **Canva design (URL, shortlink, design ID, or title):**
  - If Canva MCP tools are connected, follow [Canva Editing Protocol](./references/canva-editing-protocol.md) (Phase 1 read-only): locate design, inspect `richtexts` coordinates/links via `start-editing-transaction` and immediately `cancel-editing-transaction`, plus export high-res PNG/PDF when checking fine alignment or ATS output. If Canva MCP tools are unavailable, ask the user to export a PDF or PNG from Canva and analyze that file.
- **Image / Screenshot (`.png`, `.jpg`, `.webp`):**
  - Inspect the image visually with your file/image viewer tool and check typography, margins, spacing, alignment, and visible URLs.
- **Text / Markdown / LaTeX / Google Docs:**
  - Read the full source; if LaTeX, specifically check for `\hyphenpenalty` / hyphenation, letter-spacing macros, and page background color.

### Step 2: Score Across 8 Sections & Sub-Metrics (0–100)

Load [Scoring Rubric](./references/scoring-rubric.md) and [ATS & Visual Checks](./references/ats-and-visual-checks.md).

Evaluate each applicable section using explicit sub-metrics (`0–100`), then calculate the weighted overall score:
1. **Header & Contact Info (8%)**
2. **Profile / Summary (12%)**
3. **Technical Skills (15%)**
4. **Experience (20%)**
5. **Projects / Competitions / Open Source (18%)**
6. **Education (10%)**
7. **Languages & Volunteering / Extracurriculars (7%)**
8. **Design, Geometry & ATS Readiness (10%)**

If this is a **re-evaluation** after edits, use the **exact same weights** and show explicit `Before → After` score deltas.

### Step 3: Match Top 5 Job Positions

Load [Job Matching Guide](./references/job-matching-guide.md).

Identify the **Top 5 Job Positions** ranked by realistic interview conversion, citing concrete evidence from the CV. Clearly separate **Current Fit %** (backed by experience/projects) from **Potential Fit %** (when a skill appears in `Summary`/`Skills` without supporting projects yet).

### Step 4: Present the Report & Next Actions

Follow [Sample Report Structure](./examples/sample-report.md):
1. **Global Score (0–100)** + candidate potential summary.
2. **Critical ATS/OCR Alert** (prominently upfront if hidden text, broken links, or A3 size was detected).
3. **Section-by-Section Table** with scores, sub-metrics, and direct, concrete diagnosis.
4. **Top 5 Quick Wins** ordered by impact-to-effort ratio.
5. **Top 5 Job Positions** with evidence-backed rationale and 1-line conversion tips.
6. **Actionable Offer:** Offer to produce copy-paste **"Before → After"** rewrites per section, check a specific element (like photo/margin alignment), or—when editing a Canva design—apply safe text/alignment fixes in a previewed draft.

---

## Mode-Specific Instructions

- **If the user asks "what should I change in each section?":**
  Provide copy-paste **Before → After** rewrites for every weak bullet/section, using `[X]` placeholders for missing real metrics, plus exact spacing/layout instructions.
- **If the user asks to apply changes to Canva:**
  Follow [Canva Editing Protocol](./references/canva-editing-protocol.md) Phase 2 strictly: batch edits in a draft, verify resulting heights/wrapping, show the `get-design-thumbnail` preview, wait for explicit confirmation, then commit and share the fresh `edit_url`.
- **If the user compares multiple CVs (e.g., friends' CVs):**
  Apply the identical rubric objectively to each CV, highlight each candidate's unique unfair advantage, and warn clearly about document vs. profile gaps.
