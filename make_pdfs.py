"""
Generate lab reports as PDFs with code and outputs from C++ files.
"""

import subprocess
from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak,
    Preformatted, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

# ---------- CONFIGURATION ----------
EXTENSION = "cpp"
LOGO_PATH = "./logo.png"
PROCESS = ["Lab 5"]
EXECUTION_TIMEOUT = 5  # seconds

UNIVERSITY = "NED University of Engineering and Technology"
NAME = "Muhammad Raza"
ROLL_NO = "CT-24138"
DEPARTMENT = "Department of Computer Science and Information Technology"
DEGREE = "Bachelor of Science (BS)"

# ---------- STYLES ----------
styles = getSampleStyleSheet()
title_style = ParagraphStyle("CustomTitle", parent=styles["Title"], fontSize=28, alignment=1, spaceAfter=20)
subtitle_style = ParagraphStyle("Subtitle", parent=styles["Normal"], fontSize=16, alignment=1,
                                textColor=colors.HexColor("#333333"), spaceAfter=10)
info_style = ParagraphStyle("Info", parent=styles["Normal"], alignment=1, fontSize=12,
                            textColor=colors.HexColor("#555555"))
code_style = ParagraphStyle("CodeStyle", fontName="Courier", fontSize=9, leading=12,
                            backColor=colors.whitesmoke, borderPadding=5,
                            borderColor=colors.lightgrey, borderWidth=0.5)
terminal_style = ParagraphStyle("TerminalStyle", fontName="Courier", fontSize=9, leading=12,
                                backColor=colors.black, textColor=colors.white,
                                borderPadding=5, borderColor=colors.lightgrey, borderWidth=0.5)
heading_style = styles["Heading2"]

# ---------- HELPERS ----------
def terminal_block(text: str):
    """Return a styled terminal-like block for output text."""
    pre = Preformatted(text, terminal_style)
    table = Table([[pre]])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.black),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.whitesmoke),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("INNERPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


def compile_and_run(src_path: Path):
    """Compile and run a C++ file, returning output or error."""
    output_path = src_path.with_suffix("")  # compiled executable path
    compile_cmd = ["g++", str(src_path), "-o", str(output_path)]

    # Debug info
    print(f"Compiling: {src_path} -> {output_path}")
    print(f"Command: {' '.join(compile_cmd)}")

    try:
        start_time = datetime.now()
        subprocess.run(compile_cmd, check=True)

        result = subprocess.run(
            [str(output_path)],
            capture_output=True,
            text=True,
            timeout=EXECUTION_TIMEOUT
        )
        end_time = datetime.now()

        output = (result.stdout + result.stderr).replace(": ", ":\n").strip()
        output += f"\n[Execution Time: {(end_time - start_time).total_seconds():.2f}s]"

        return output, None

    except subprocess.TimeoutExpired:
        return None, "⏱️ Execution timed out (program may be waiting for input)."
    except subprocess.CalledProcessError as e:
        return None, f"❌ Compilation or execution failed:\n{e.stderr or str(e)}"


def build_title_page(lab_name: str):
    """Build the title page for a lab report."""
    return [
        Spacer(1, 2 * inch),
        Image(LOGO_PATH, width=2.5 * inch, height=2.5 * inch),
        Spacer(1, 0.5 * inch),
        Paragraph(UNIVERSITY, title_style),
        Paragraph("Data Structures and Algorithms", subtitle_style),
        Spacer(1, 0.5 * inch),
        Paragraph(f"Author: {NAME}", info_style),
        Paragraph(f"Roll No: {ROLL_NO}", info_style),
        Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", info_style),
        Spacer(1, 1.9 * inch),
        Paragraph(f"{DEPARTMENT}<br/>{DEGREE}", info_style),
        PageBreak()
    ]


def build_question_block(n: int, src_path: Path):
    """Build a block containing question code and its output/error."""
    block = [Paragraph(f"Question {n+1}", heading_style)]
    with open(src_path, 'r', encoding="utf-8") as f:
        block.append(Preformatted(f.read(), code_style))

    output, error = compile_and_run(src_path)
    if output:
        block.append(Paragraph("Output", heading_style))
        block.append(terminal_block(output))
    else:
        block.append(Paragraph("Error", heading_style))
        block.append(terminal_block(error))

    block.append(Spacer(1, 0.5 * inch))
    return block

# ---------- MAIN ----------
for lab_name in PROCESS:
    lab_path = Path(f"./{lab_name}")
    lab_path.mkdir(parents=True, exist_ok=True)
    pdf_path = lab_path / f"{ROLL_NO}_{lab_name}.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)
    content = build_title_page(lab_name)

    files = sorted(lab_path.glob(f"*.{EXTENSION}"))
    for q_index, src_path in enumerate(files):
        content.extend(build_question_block(q_index, src_path))

    doc.build(content)
    print(f"✅ PDF of {lab_name} created successfully: {pdf_path}")
