#!/usr/bin/env python3
"""Zero-dependency forensic ATS and structure auditor for CV PDF files.

Uses only the Python standard library to inspect page dimensions (A4/Letter/A3),
embedded URI links, fonts, PDF structure tags (/StructTreeRoot), MCID stream
ordering, and potential hidden-text / white-fonting ATS traps. If ``pypdf``,
``fitz`` (PyMuPDF), or ``pdftotext`` is available, it also checks extracted
plain text for letter-spaced headings and hyphenation word-splits.

Usage:
    python audit_pdf_ats.py path/to/cv.pdf [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import zlib
from pathlib import Path
from typing import Any


PAGE_SIZE_PRESETS = [
    ("A4", 595.0, 842.0),
    ("US Letter", 612.0, 792.0),
    ("A3", 842.0, 1191.0),
]


def classify_page_size(width_pt: float, height_pt: float) -> str:
    """Return a human-readable page size label from PDF points."""
    for name, w, h in PAGE_SIZE_PRESETS:
        if (abs(width_pt - w) < 12 and abs(height_pt - h) < 12) or (
            abs(width_pt - h) < 12 and abs(height_pt - w) < 12
        ):
            orientation = "Portrait" if height_pt >= width_pt else "Landscape"
            return f"{name} ({orientation}, {width_pt:.0f}x{height_pt:.0f} pt)"
    return f"Custom ({width_pt:.0f}x{height_pt:.0f} pt)"


def parse_pdf_objects(raw: bytes) -> dict[int, bytes]:
    """Extract numbered indirect objects from raw PDF bytes."""
    return {
        int(m.group(1)): m.group(2)
        for m in re.finditer(rb"(\d+)\s+\d+\s+obj\b(.*?)endobj", raw, re.S)
    }


def decode_stream(obj_body: bytes) -> bytes:
    """Decompress a PDF object stream if zlib-compressed; return raw stream otherwise."""
    m = re.search(rb"stream\r?\n(.*?)\r?\nendstream", obj_body, re.S)
    if not m:
        return b""
    payload = m.group(1)
    try:
        return zlib.decompress(payload)
    except zlib.error:
        return payload


def extract_struct_mcids(objs: dict[int, bytes]) -> list[tuple[str, int]]:
    """Walk /StructTreeRoot (if present) and return (tag, mcid) reading order."""
    root_id = None
    for oid, body in objs.items():
        if b"/Type /StructTreeRoot" in body or b"/Type/StructTreeRoot" in body:
            root_id = oid
            break
    if root_id is None:
        return []

    visited: set[int] = set()
    sequence: list[tuple[str, int]] = []

    def walk(oid: int) -> None:
        if oid in visited or oid not in objs:
            return
        visited.add(oid)
        text = objs[oid].decode("latin1", errors="replace")
        tag_match = re.search(r"/S\s*/(\w+)", text)
        tag = tag_match.group(1) if tag_match else "Elem"
        k_match = re.search(r"/K\s*(\[.*?\]|\d+\s+\d+\s+R|\d+)", text, re.S)
        if not k_match:
            return
        k_val = k_match.group(1)
        if k_val.startswith("["):
            tokens = re.findall(r"(\d+\s+\d+\s+R|\d+)", k_val)
            for tok in tokens:
                if tok.endswith("R"):
                    walk(int(tok.split()[0]))
                else:
                    sequence.append((tag, int(tok)))
        elif k_val.endswith("R"):
            walk(int(k_val.split()[0]))
        else:
            sequence.append((tag, int(k_val)))

    walk(root_id)
    return sequence


def extract_optional_plain_text(pdf_path: Path) -> tuple[str | None, str | None]:
    """Try optional host PDF text extractors without failing if absent."""
    if shutil.which("pdftotext"):
        try:
            proc = subprocess.run(
                ["pdftotext", str(pdf_path), "-"],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            if proc.returncode == 0 and proc.stdout.strip():
                return proc.stdout, "pdftotext"
        except Exception:
            pass

    for mod_name in ("pypdf", "PyPDF2", "fitz"):
        try:
            mod = __import__(mod_name)
            if mod_name == "fitz":
                doc = mod.open(str(pdf_path))
                return "\n".join(page.get_text("text") for page in doc), "pymupdf"
            reader = mod.PdfReader(str(pdf_path))
            return "\n".join(page.extract_text() or "" for page in reader.pages), mod_name
        except Exception:
            continue

    return None, None


def analyze_extracted_text(text: str) -> dict[str, Any]:
    """Detect common ATS text pitfalls in extracted plain text."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    letter_spaced = [
        line
        for line in lines
        if re.fullmatch(r"(?:[A-Z]\s+){3,}[A-Z](?:\s{2,}(?:[A-Z]\s+){2,}[A-Z])*", line)
    ]
    hyphen_splits = re.findall(r"\b([A-Za-z]{2,})-\s*\n\s*([a-z]{2,})\b", text)
    urls_in_text = re.findall(
        r"(?:https?://)?(?:www\.)?(?:linkedin\.com/in/[A-Za-z0-9_.-]+|github\.com/[A-Za-z0-9_.-]+)",
        text,
        re.I,
    )
    return {
        "letter_spaced_headings": letter_spaced,
        "hyphenated_line_breaks": [f"{a}-{b}" for a, b in hyphen_splits],
        "visible_profile_urls": sorted(set(urls_in_text)),
        "first_5_lines": lines[:5],
    }


def audit_pdf(pdf_path: Path) -> dict[str, Any]:
    """Run all stdlib and optional ATS checks on a PDF file."""
    raw = pdf_path.read_bytes()
    objs = parse_pdf_objects(raw)

    # Page count and dimensions (/MediaBox)
    page_boxes: list[str] = []
    for body in objs.values():
        if re.search(rb"/Type\s*/Page\b(?!s)", body):
            mb = re.search(
                rb"/MediaBox\s*\[\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\]",
                body,
            )
            if mb:
                x0, y0, x1, y1 = (float(mb.group(i)) for i in range(1, 5))
                page_boxes.append(classify_page_size(abs(x1 - x0), abs(y1 - y0)))
    if not page_boxes:
        for mb in re.finditer(
            rb"/MediaBox\s*\[\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\]", raw
        ):
            x0, y0, x1, y1 = (float(mb.group(i)) for i in range(1, 5))
            page_boxes.append(classify_page_size(abs(x1 - x0), abs(y1 - y0)))

    # Embedded clickable links
    uris = sorted(
        {
            m.decode("latin1", errors="replace")
            for m in re.findall(rb"/URI\s*\(([^)]+)\)", raw)
        }
    )

    # Embedded font names
    fonts = sorted(
        {
            re.sub(r"^[A-Z]{6}\+", "", m.decode("latin1", errors="replace"))
            for m in re.findall(rb"/BaseFont\s*/([^\s/\[\]<>()]+)", raw)
        }
    )

    # Zero-opacity graphics states and stream heuristics
    zero_opacity_gs_ids: set[str] = set()
    zero_opacity_gs: list[str] = []
    for oid, body in objs.items():
        if re.search(rb"/ca\s+0(?:\.0+)?\b", body) or re.search(rb"/CA\s+0(?:\.0+)?\b", body):
            zero_opacity_gs.append(f"obj {oid}")
            zero_opacity_gs_ids.add(str(oid))

    # Map graphics-state resource names (e.g. /gs2 -> 89) to detect zero-opacity text
    zero_opacity_res_names: set[str] = set()
    for body in objs.values():
        for gm in re.finditer(rb"/([A-Za-z0-9_]+)\s+(\d+)\s+\d+\s+R", body):
            if gm.group(2).decode("latin1") in zero_opacity_gs_ids:
                zero_opacity_res_names.add(gm.group(1).decode("latin1"))

    tiny_font_calls = 0
    invisible_render_mode = 0
    white_fill_near_text = 0
    zero_opacity_near_text = 0
    stream_mcids: list[int] = []

    for body in objs.values():
        dec = decode_stream(body)
        if not dec:
            continue
        text_stream = dec.decode("latin1", errors="replace")
        if "/MCID" in text_stream:
            stream_mcids.extend(int(m) for m in re.findall(r"/MCID\s+(\d+)", text_stream))
        if "BT" in text_stream:
            for fm in re.finditer(r"/F\d+\s+([\d.]+)\s+Tf", text_stream):
                if float(fm.group(1)) < 4.0:
                    tiny_font_calls += 1
            if re.search(r"\b3\s+Tr\b", text_stream):
                invisible_render_mode += 1
            if re.search(r"(?:1\s+1\s+1\s+rg|1\s+g|0\s+0\s+0\s+0\s+k)\s+(?:[^\n]*\n){0,4}\s*BT", text_stream):
                white_fill_near_text += 1
            for gs_name in zero_opacity_res_names:
                if re.search(rf"/{re.escape(gs_name)}\s+gs\s+(?:[^\n]*\n){{0,4}}\s*BT", text_stream):
                    zero_opacity_near_text += 1

    struct_seq = extract_struct_mcids(objs)
    struct_mcids = [mcid for _, mcid in struct_seq]
    is_tagged = bool(struct_seq)

    # Check if tagged order diverges from raw content stream order
    tagged_vs_stream_reordered = False
    if struct_mcids and stream_mcids:
        common_struct = [m for m in struct_mcids if m in set(stream_mcids)]
        tagged_vs_stream_reordered = common_struct != sorted(common_struct)

    plain_text, extractor = extract_optional_plain_text(pdf_path)
    text_analysis = analyze_extracted_text(plain_text) if plain_text else None

    warnings: list[str] = []
    if not is_tagged:
        warnings.append("PDF is untagged (no /StructTreeRoot); ATS relies solely on raw stream order.")
    if tagged_vs_stream_reordered:
        warnings.append(
            "Tagged reading order differs from raw PDF stream order; legacy ATS without Structure Tree support may read blocks out of order."
        )
    if not uris:
        warnings.append("No clickable /URI annotations detected in PDF; verify social/portfolio links.")
    if tiny_font_calls > 0 or invisible_render_mode > 0 or white_fill_near_text > 0 or zero_opacity_near_text > 0:
        warnings.append(
            "Potential hidden-text pattern detected (tiny font <4pt, Tr 3 invisible mode, zero-opacity gs, or white fill near text). Verify no white-font ATS stuffing exists."
        )
    for size in page_boxes:
        if size.startswith("A3 "):
            warnings.append(
                f"Page size is {size} instead of standard A4 or US Letter; check export/canvas dimensions."
            )
    if text_analysis:
        if text_analysis["letter_spaced_headings"]:
            warnings.append(
                f"Letter-spaced headings detected ({text_analysis['letter_spaced_headings']}); some ATS parsers fail to match spaced words."
            )
        if text_analysis["hyphenated_line_breaks"]:
            warnings.append(
                f"Hyphenated line breaks detected ({text_analysis['hyphenated_line_breaks']}); split words can break keyword search."
            )

    return {
        "file": str(pdf_path),
        "bytes": len(raw),
        "page_count": len(page_boxes) if page_boxes else None,
        "page_sizes": page_boxes,
        "is_tagged_pdf": is_tagged,
        "embedded_uris": uris,
        "fonts": fonts,
        "raw_mcid_count": len(stream_mcids),
        "tagged_mcid_count": len(struct_mcids),
        "tagged_vs_stream_reordered": tagged_vs_stream_reordered,
        "suspicious_signals": {
            "zero_opacity_extgstate": zero_opacity_gs,
            "zero_opacity_near_text": zero_opacity_near_text,
            "tiny_font_calls_under_4pt": tiny_font_calls,
            "invisible_text_render_mode": invisible_render_mode,
            "white_fill_before_bt": white_fill_near_text,
        },
        "text_extractor_used": extractor,
        "extracted_text_checks": text_analysis,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a CV PDF for ATS and layout risks.")
    parser.add_argument("pdf_path", type=Path, help="Path to the CV PDF file")
    parser.add_argument("--json", action="store_true", help="Print output as JSON")
    args = parser.parse_args()

    if not args.pdf_path.is_file():
        print(f"Error: File not found: {args.pdf_path}", file=sys.stderr)
        return 1

    report = audit_pdf(args.pdf_path)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"=== PDF ATS Audit: {report['file']} ===")
        print(f"Size: {report['bytes']} bytes | Pages: {report['page_count']} | Format: {report['page_sizes']}")
        print(f"Tagged PDF (/StructTreeRoot): {report['is_tagged_pdf']}")
        print(f"Embedded URI links ({len(report['embedded_uris'])}): {report['embedded_uris']}")
        print(f"Fonts: {report['fonts']}")
        print(f"Tagged order differs from raw stream: {report['tagged_vs_stream_reordered']}")
        print(f"Suspicious signals: {report['suspicious_signals']}")
        if report["extracted_text_checks"]:
            print(f"Text extractor: {report['text_extractor_used']}")
            print(f"Letter-spaced headings: {report['extracted_text_checks']['letter_spaced_headings']}")
            print(f"Hyphenated splits: {report['extracted_text_checks']['hyphenated_line_breaks']}")
            print(f"Visible profile URLs: {report['extracted_text_checks']['visible_profile_urls']}")
        if report["warnings"]:
            print("\nWarnings:")
            for w in report["warnings"]:
                print(f"  - {w}")
        else:
            print("\nNo ATS structural warnings detected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
