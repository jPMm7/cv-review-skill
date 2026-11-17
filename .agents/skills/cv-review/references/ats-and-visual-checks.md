# ATS, OCR, and Visual Geometry Checks

Always inspect **both** the rendered appearance (what humans see) **and** the underlying text/PDF structure (what ATS parsers and OCR extract).

---

## 1. Visual Geometry & Layout Checklist

Inspect the rendered image or element bounding boxes for:

1. **Page Size & Format:**
   - Confirm standard **A4** (`595 x 842 pt`, or `794 x 1123 px` at 96 dpi) for EU/international, or **US Letter** (`612 x 792 pt`).
   - Watch out for **Canva A3 traps** (`842 x 1190 pt` / `1123 x 1587 px` — looks like A4 proportions on screen, exports at A3 poster dimensions!).
2. **Unified Margin Grid:**
   - Every section header, company title, project block, and education entry should share the **exact same left margin** (`±2px`) and **right margin**.
   - Watch out for leftover template indentations (e.g., `Projects` or `Education` shifted 40–60px right from removing timeline icons).
3. **Orphan Elements & Collisions:**
   - Check for floating dates left behind when deleting an entry (e.g., a stray `"July 2026"` floating above `Education`).
   - Check for overlapping/duplicate images behind profile photos (creating thin border strips) or photos touching the top page edge (`< 15px` margin).
   - Check for two-column sections where the right column starts on the same baseline as the section header.
   - Check bottom margin (`>= 25–30px` clear breathing room so text never clips on print/export).
4. **Visual Scannability & Print Safety:**
   - Prefer **pure white background (`#FFFFFF`)** over grey/tinted backgrounds (avoids ugly printer margins and saves ink).
   - Maintain clear typographic hierarchy (Name > Section Headings > Subheadings/Roles > Body), consistent bullet symbols (`•` everywhere, never mixing `•` and `○` arbitrarily), and subtle horizontal section dividers where helpful.
   - Avoid `"Personal Portfolio Website: in development"` or broken/dead links.

---

## 2. PDF / ATS Forensic Checklist

When evaluating a `.pdf` file (or exporting one from Canva), run `scripts/audit_pdf_ats.py` and inspect OCR/text output for:

1. **Hidden / White-Font Text ("White-Fonting"):**
   - Compare the **OCR / extracted text** against the **rendered page image**.
   - Any text appearing in OCR that is NOT visible on the page (white text on white background, `< 4pt` font, `ca 0.0` opacity, or off-canvas text) is a **Critical Red Flag**: modern ATS platforms flag and reject white-fonting as keyword stuffing, and human reviewers viewing plain-text imports see unformatted spam.
2. **Icon-Only Social Links:**
   - Check whether `GitHub`, `LinkedIn`, and `Portfolio` show readable handles/URLs (`linkedin.com/in/handle`, `github.com/handle`) **and** embed real `/URI` PDF annotations.
   - Icon-only links turn into garbage glyphs (`§ ï`) in OCR and break completely when printed.
3. **Letter-Spaced Headings:**
   - Avoid styling headings with literal spaces (`S U M M A R Y`, `E X P E R I E N C E`, `S K I L L S`). OCR/ATS reads them as single letters and fails section classification. Use CSS/LaTeX letter-spacing (`letter-spacing` / `soul` carefully) or standard uppercase (`EXPERIENCE`) instead.
4. **Automatic Hyphenation Across Line Breaks:**
   - Words broken mid-word (`intern-ship`, `Pre-cision`, `ros-bags`, `pre-sentation`) split ATS keywords in plain-text extraction. Disable hyphenation (`\usepackage[none]{hyphenat}` or `\hyphenpenalty=10000` in LaTeX; widen text boxes in Canva).
5. **Superscript Splitting:**
   - Superscripts like `1st` / `2nd` often extract as `1 Place` / `st` on separate lines. Plain `1st` / `2nd` (without superscript tags) avoids extraction glitches.
6. **Tagged PDF vs Raw Stream Reading Order:**
   - Canva exports a `/StructTreeRoot` (Tagged PDF) which usually follows top-to-bottom reading order, **but** the raw PDF content stream follows layer creation/edit order.
   - Advise the user to verify with `Ctrl+A` → `Ctrl+C` → Notepad on the exported PDF, and reorder layers top-to-bottom (`Position → Layers`) in Canva if legacy ATS compatibility matters.

---

## 3. Regional Conventions (EU vs US/UK/Remote)

- **Portugal / Continental Europe:** A4 format; concise professional headshot is acceptable (ensure clean framing and balanced margins); CEFR language levels (`C1/C2`, `B1/B2`) are standard and valued.
- **US / UK / Big Tech / Remote Global:** Omit photos, date of birth, and marital status to avoid unconscious bias and ATS image clutter; US Letter or A4 accepted; keep 1 page for < 7–10 years experience.
