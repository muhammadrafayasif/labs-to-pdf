"""
Generate lab reports as PDFs with code and outputs from C++ files.
"""

import subprocess, os
from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak,
    Preformatted, Table, TableStyle, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

# ---------- CONFIGURATION ----------
EXTENSION = "cpp"
LOGO_PATH = "./logo.png"
PROCESS = ["Lab 1"] # Folder names, must match exactly
KEEP_TOGETHER = True # Skip to next page if the question starts at the end of page
KEEP_EXE = False # Remove or keep the .exe file generated automatically

""" Enter the user inputs for each lab in the following order:  
    INPUTS = [
        [Q1 INPUTS, Q2 INPUTS, Q3 INPUTS, ...], # For Lab 1 (According to the first lab provided in the PROCESS list)
        [Q1 INPUTS, Q2 INPUTS, Q3 INPUTS, ...], # For Lab 2 (According to the second lab provided in the PROCESS list)
        ...
    ]

    For example, If Q2 does not take input, leave it as an empty string
    ["2 2", "", "1 4"]
"""
INPUTS = [
    
]

""" The QUESTIONS list follows the same format as the INPUT list provided above """
QUESTIONS = [
    
]

EXECUTION_TIMEOUT = 5  # seconds

UNIVERSITY = "NED University of Engineering and Technology"
NAME = "NAME"
ROLL_NO = "CT-24000"
DEPARTMENT = "Department of Computer Science and Information Technology"
DEGREE = "Bachelor of Science (BS)"

# ---------- STYLES ----------
pdfmetrics.registerFont(TTFont("CustomFont", "font.ttf"))
styles = getSampleStyleSheet()
title_style = ParagraphStyle("Title", fontName="CustomFont", parent=styles["Title"], fontSize=28, alignment=1, spaceAfter=20)
subtitle_style = ParagraphStyle("Subtitle",fontName="CustomFont", parent=styles["Normal"], fontSize=16, alignment=1,
                                textColor=colors.HexColor("#333333"), spaceAfter=10)
info_style = ParagraphStyle("Info", fontName="CustomFont", parent=styles["Normal"], alignment=0, fontSize=12,
                            textColor=colors.HexColor("#555555"))
footer_style = ParagraphStyle("Info", fontName="CustomFont", parent=styles["Normal"], alignment=1, fontSize=12,
                            textColor=colors.HexColor("#555555"))
code_style = ParagraphStyle("CodeStyle", fontName="Courier", fontSize=9, leading=12,
                            backColor=colors.whitesmoke, borderPadding=5,
                            borderColor=colors.lightgrey, borderWidth=0.5)
terminal_style = ParagraphStyle("TerminalStyle", fontName="Courier", fontSize=9, leading=12,
                                backColor=colors.black, textColor=colors.white,
                                borderPadding=5, borderColor=colors.lightgrey, borderWidth=0.5)
question_style = ParagraphStyle("Question", parent=styles["Normal"])

# ---------- HELPERS ----------
def terminal_block(text: str, input: str = "") -> Table:
    """Return a styled terminal-like block for output text."""
    text += f"\n[INPUT PROVIDED]\n{input}"
    pre = Preformatted(text, terminal_style)
    table = Table([[pre]])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.black),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.whitesmoke),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("INNERPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


def compile_and_run(src_path: Path, input: str = "", keep_exe: bool = False, debug: bool = False) -> str | None:
    """Compile and run a C++ file, returning output or error with robust handling."""
    output_path = src_path.with_suffix("")  # compiled executable path
    compile_cmd = ["g++", str(src_path), "-o", str(output_path)]

    # Debug info
    if debug:
        print(f"Compiling: {src_path} -> {output_path}")
        print(f"Command: {' '.join(compile_cmd)}")

    try:
        start_time = datetime.now()
        # Compile the source file
        subprocess.run(compile_cmd, check=True)

        # Run the compiled program with a generous timeout
        result = subprocess.run(
            [str(output_path)],
            capture_output=True,
            input=input,
            text=True,
            timeout=60  # best practice: allow up to 60s for long-running programs
        )
        end_time = datetime.now()

        # Remove generated .exe file if permitted
        if not keep_exe:
            os.remove(output_path.with_suffix(".exe"))

        # Collect both stdout and stderr
        output = (result.stdout + result.stderr).replace(": ", ":\n").strip()
        output += f"\n[Execution Time: {(end_time - start_time).total_seconds():.2f}s]"

        return output, None

    except subprocess.TimeoutExpired:
        return None, "⏱️ Execution timed out (program may be waiting for input or running too long)."
    except subprocess.CalledProcessError as e:
        return None, f"❌ Compilation or execution failed:\n{e.stderr or str(e)}"

def build_title_page(lab_name: str):
    """Build the title page for a lab report."""
    return [
        Spacer(1, 2 * inch),
        Image(LOGO_PATH, width=2.5 * inch, height=2.5 * inch),
        Spacer(1, 0.5 * inch),
        Paragraph(UNIVERSITY, title_style),
        Paragraph(f"Data Structures and Algorithms — {lab_name}", subtitle_style),
        Spacer(1, 0.5 * inch),
        Paragraph(f"Author: {NAME}", info_style),
        Paragraph(f"Roll No: {ROLL_NO}", info_style),
        Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", info_style),
        Spacer(1, 1.9 * inch),
        Paragraph(f"{DEPARTMENT}<br/>{DEGREE}", footer_style),
        PageBreak()
    ]


def build_question_block(lab_index: int, n: int, src_path: Path, keep_together: bool = True) -> list:
    """Build a block containing question code and its output/error."""
    lab = [Paragraph(f"Question {n+1}", title_style)]
    
    # Safely get the question text
    question_text = QUESTIONS[lab_index][n] if lab_index < len(QUESTIONS) and n < len(QUESTIONS[lab_index]) else None
    
    # Only add if the question exists and is not empty
    if question_text:
        lab.append(Paragraph(question_text, question_style))
        lab.append(Spacer(1, 0.2 * inch))
    
    with open(src_path, 'r', encoding="utf-8") as f:
        lab.append(Preformatted(f.read(), code_style))

    input = INPUTS[lab_index][n] if lab_index < len(INPUTS) and n < len(INPUTS[lab_index]) else None
    output, error = compile_and_run(src_path, input=input, keep_exe=KEEP_EXE)
    if output:
        lab.append(Paragraph("Output", title_style))
        lab.append(terminal_block(output, input))
    else:
        lab.append(Paragraph("Error", title_style))
        lab.append(terminal_block(error))

    return [KeepTogether(lab)] if keep_together else lab

# ---------- MAIN ----------
for lab_index, lab_name in enumerate(PROCESS):
    lab_path = Path(f"./{lab_name}")
    lab_path.mkdir(parents=True, exist_ok=True)
    pdf_path = lab_path / f"{ROLL_NO}_{lab_name.replace(" ","")}.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)
    content = build_title_page(lab_name)

    files = sorted(lab_path.glob(f"*.{EXTENSION}"))
    for q_index, src_path in enumerate(files):
        content.extend(build_question_block(lab_index, q_index, src_path, KEEP_TOGETHER))

    doc.build(content)
    print(f"✅ PDF of {lab_name} created successfully: {pdf_path}")
