# Safe Canva Inspection & Editing Protocol

Use this protocol whenever the target CV lives in **Canva** and the Canva MCP tools are available (`search-designs`, `get-design`, `get-design-content`, `start-editing-transaction`, `perform-editing-operations`, `get-design-thumbnail`, `commit-editing-transaction`, `cancel-editing-transaction`, `export-design`).

---

## Phase 1: Read-Only Inspection (Default for Review/Evaluation)

1. **Locate the design:**
   - If given a design ID (`D...`), URL, or shortlink, resolve directly (`resolve-shortlink` if shortlink).
   - If given only a title (e.g., `"João Marques CV"`), call `search-designs`.
2. **Fetch metadata, text, and high-res visual:**
   - Call `get-design` (check title, page count, `edit_url`).
   - Call `start-editing-transaction` to obtain every `richtext` element (`element_id`, exact `position`, `dimension`, `formatting.link`), image `fills`, `pages` dimensions, and a rendered preview thumbnail.
   - **Immediately call `cancel-editing-transaction`** once inspection data is captured — never leave a read-only transaction open!
   - Optional (recommended for tiny text/divider inspection and real ATS audit): call `export-design` (`png` at `width: 1600` and/or `pdf`), download locally, inspect the PNG with `read_file`, and run `scripts/audit_pdf_ats.py` on the PDF.
3. **Spot Canva-specific geometry & link traps:**
   - Check whether links (`LinkedIn`, `GitHub`) are attached to the **visible text run** or to an empty anchor (`Linkedin[]`).
   - Compare `left` coordinates across all body blocks and section headings (`±2px` target).
   - Check `top + height` of bottom elements against `pages[0].dimension.height`.
   - Look for stacked duplicate `fills` around profile photos and orphan date elements.

---

## Phase 2: Safe Draft-Preview-Approve Edits (Only When User Requests Changes)

Follow a strict **Start → Edit → Preview → Explicit Approval → Commit** flow:

1. **Know the Canva API limits (`CAN` vs `CANNOT`):**
   - **CAN:** `replace_text`, `find_and_replace_text` (prefer this to preserve partial bold/italic spans!), `format_text` (links, underline, weight, color, alignment), `position_element`, `resize_element` (width only for text), `delete_element`, `update_title`.
   - **CANNOT:** Add new text boxes, draw vector divider lines/shapes, change font family/typeface, reorder layers (`Position → Layers`), change page background color, or add/delete pages.
   - **Never hack around `CANNOT` items** (e.g., never pad spaces inside a left title box to simulate a right-aligned date box). Tell the user clearly how to do those in 10 seconds inside the Canva UI.
2. **Batch operations cleanly:**
   - Start a fresh `start-editing-transaction`, read the returned `transaction_id` and `pages` array.
   - Apply edits in one batched `perform-editing-operations` call where possible.
   - Check the returned element `height` values to make sure edited text did not wrap unexpectedly or collide with elements below — adjust positions of lower elements if height changed.
3. **Preview & Explicit Approval Gate (Mandatory):**
   - Always call `get-design-thumbnail` after edits, inspect the returned image via `read_file` to verify zero overlaps, and **show the thumbnail preview URL to the user** along with a plain-language list of every draft change.
   - Never call `commit-editing-transaction` without explicit user confirmation (e.g., `"confirmo"`, `"guarda"`, `"sim"`).
4. **Commit & Share Direct Link:**
   - After explicit approval, call `commit-editing-transaction`.
   - Call `get-design` and share the fresh clickable `edit_url` so the user can open and refresh their design immediately.
