# CV Scoring Rubric (0–100)

Score each section independently from **0 to 100** using explicit sub-metrics, then compute the weighted overall score. Never inflate scores to be polite — always ground every deducted point in direct observations from the CV's text, geometry, or PDF/OCR layer.

---

## Calibration Bands

| Band | Meaning |
| :--- | :--- |
| **90–100** | **Elite / Interview-ready.** Quantified impact, spotless writing, ATS-safe PDF, unified visual grid, strong proof for every claim. |
| **80–89** | **Strong & ready to send.** Competitive for target roles, clean formatting, minor optional optimizations only. |
| **70–79** | **Solid foundation with clear gaps.** Good raw profile held back by missing metrics, unbacked skill claims, typos, or layout glitches. |
| **55–69** | **High potential, under-performing document.** Strong background undermined by serious ATS traps (hidden text, icon-only links, scrambled OCR), missing core sections (e.g., Projects/Languages), or sloppy polish. |
| **< 55** | **Needs structural rebuild** before sending to recruiters. |

---

## Standard Section Weights

Use these default weights (total = 100%). Adjust only if a section genuinely does not apply to the candidate's career stage (e.g., experienced senior engineers may omit `Languages & Volunteering` or merge `Projects` into `Experience` — redistribute cleanly so weights still sum to 100%).

| Section | Weight | Sub-metrics (0–100 each) | What separates 60 vs 90+ |
| :--- | :---: | :--- | :--- |
| **1. Header & Contact Info** | **8%** | • Visual Hierarchy & Framing<br>• Link Visibility, Clickability & Completeness | **90+:** Name + clear target title; top-of-page contacts; international phone (`+XXX`); clean email; full visible + clickable URLs (`linkedin.com/in/...`, `github.com/...`); no `"in development"` placeholders; appropriate photo framing (if EU/local) or no photo (if US/UK).<br>**<65:** Contacts buried in footer, icon-only links missing text URLs, missing country code, overlapping/cropped photo, broken anchor links. |
| **2. Profile / Summary** | **12%** | • Positioning & Focus<br>• Conciseness & Language<br>• Consistency with Rest of CV | **90+:** 2–4 crisp lines; idiomatic grammar; active tone; zero buzzword fluff (`"cutting-edge"`, `"rockstar"`); **every major claim (e.g., AI agents, Master's degree) is backed up below**.<br>**<70:** Wordy 5+ line wall of text; non-idiomatic phrasing (`"expected to end at"`); timid phrasing (`"some hands-on experience"`); promises skills/degrees missing from `Projects`/`Education`. |
| **3. Technical Skills** | **15%** | • Organization & Scannability<br>• Accuracy & Evidence Alignment | **90+:** Logical categories (`Languages`, `AI/ML`, `Frameworks & APIs`, `Databases`, `Tools & DevOps`); zero duplicates; zero basic IDE filler (`VS Code`, `IntelliJ`); technologies match projects/experience; accurate taxonomy (`SQL` not `SQLite` as a language, `REST APIs` not a framework).<br>**<65:** Missing visually or hidden in PDF; generic `Soft Skills` bullet; unbacked buzzwords; duplicated terms; dumping tools into `Other Tools`. |
| **4. Experience** | **20%** | • Technical Depth & Action Verbs<br>• Quantified Impact & Metrics<br>• Grammar, Dates & Formatting | **90+:** Strong action verbs; concrete scale/results (`<50ms`, `60 FPS`, `% time saved`, `100+ users`, `X students/teams`); consistent date ranges (`Month YYYY – Month YYYY` or `Present`); uniform punctuation; zero typos.<br>**<70:** Zero numbers; vague claims (`"very low latency"`, `"Used Python"`); missing dates (e.g., on TA roles); typos (`"Colaborated"`, duplicated words); single-month ambiguous dates (`"July, 2026"`). |
| **5. Projects / Competitions / Open Source** | **18%** | • Technical Signal & Impact<br>• Completeness, Links & Clarity | **90+:** Multiple strong entries (or singular heading if 1); live GitHub/demo/PR links; concrete personal contributions in Open Source (never just describing what the library is); quantified metrics; clean alignment.<br>**<65:** Section missing entirely for a student/junior; plural `"Selected Projects"` with 1 entry; orphan dates; missing links; vague Open Source descriptions (`"60k+ stars"` without stating what you built). |
| **6. Education** | **10%** | • Completeness & Chronology<br>• Presentation & Alignment | **90+:** Reverse chronological; all current + completed degrees listed (e.g., M.Sc. expected + B.Sc. range); official programme names/acronyms; strong GPA highlighted cleanly (`GPA: 17/20 (A)`); relevant coursework.<br>**<70:** Missing ongoing Master's cited in Summary; missing dates; inconsistent degree names (`Master in` vs `Bachelor of`); indented inconsistently. |
| **7. Languages & Volunteering / Extracurriculars** | **7%** | • Clarity & Differentiators<br>• Layout & Margins | **90+:** Clear CEFR proficiency (`Native`, `Fluent C1/C2`, `Intermediate B1/B2`); concise leadership/community impact with scale (`1000+ attendees`, `2 academic years`); cleanly separated from Education.<br>**<65:** Languages missing entirely; missing proficiency levels; bottom-edge text overflow/clipping. |
| **8. Design, Geometry & ATS Readiness** | **10%** | • Visual Aesthetics & Grid<br>• Print Safety & Whitespace<br>• ATS / OCR Parseability | **90+:** 1-page discipline (students/early-career) or clean 2-page (senior); unified left/right margins (`±2px`); consistent vertical rhythm; white print-friendly background; **verified** A4/Letter page size; zero hyphenation splits; zero letter-spaced headings; clickable `/URI` annotations; clean top-to-bottom reading order with zero hidden text.<br>**<65:** Hidden white-font/off-canvas text traps; letter-spaced headers (`S U M M A R Y`); word-splitting hyphenation (`Pre-cision`); icon-only social links turning into garbage symbols in OCR; A3 page size export. |

---

## Edge-Case Scoring Rules

1. **Missing `Projects` section (students / interns / < 2 yrs experience):**
   - Score `Projects` at **30–40/100** (only partial credit if practical engineering builds appear inside `Experience` or `Competitions`). Do not silently drop the weight unless the candidate has 3+ years of full-time industry roles.
2. **Missing `Languages` section (non-native English / EU / international applications):**
   - Score `Languages` at **0/100** (when standalone) or deduct heavily from `Header/Skills` if missing, because European/remote recruiters verify working English immediately.
3. **Hidden / Invisible `Skills` or Text Layer Traps:**
   - If skills exist in PDF OCR/text layer but are invisible on the page (white-fonting / off-page / `0` opacity), score `Technical Skills` **<= 25/100** and flag a **Critical ATS Rejection Risk** upfront.
4. **Re-evaluation Consistency:**
   - When re-evaluating a revised CV in the same conversation, keep the **exact same weights** and report explicit `Before → After` deltas per section and globally.
