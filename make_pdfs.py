"""
Generate lab reports as PDFs with code and outputs from source files.
"""

import re
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
EXTENSION = "py"
# Set COMPILED to False when using interpreted languages like Python
COMPILED = False

LOGO_PATH = "./logo.png"

# The complete command for program compilation/interpretation
# Keep in mind that src_path and output_path are constants the program will replace 
# For python, replace with ["python", "output_path"]
# For C++, replace with ["gcc", "src_path", "-o", "output_path"]
COMPILE_CMD = ["python", "output_path"]

PROCESS = ["Lab 2"] # Folder names, must match exactly
KEEP_TOGETHER = False # Skip to next page if the question starts at the end of page
KEEP_EXE = False # Remove or keep the .exe file generated automatically (On COMPILED = True only)

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
COURSE = "Programming for AI (PAI)"

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
question_style = ParagraphStyle("Question", parent=styles["Heading5"], alignment=1)

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
    """Compile and run a file, returning output or error with robust handling."""
    if COMPILED: output_path = src_path.with_suffix("")  # compiled executable path
    else: output_path = src_path
    compile_cmd = COMPILE_CMD
    for n, i in enumerate(compile_cmd):
        if i == "src_path":
            compile_cmd[n] = str(src_path)
        elif i == "output_path":
            compile_cmd[n] = str(output_path)

    # Debug info
    if debug:
        print(f"Compiling: {src_path} -> {output_path}")
        print(f"Command: {' '.join(compile_cmd)}")

    try:
        start_time = datetime.now()

        # Compile the source file
        result = subprocess.run(compile_cmd, capture_output=True, input=input, text=True, timeout=60, check=True)
        
        # Run the compiled program with a generous timeout
        if COMPILED:
            result = subprocess.run(
                [str(output_path)],
                capture_output=True,
                input=input,
                text=True,
                timeout=60  # best practice: allow up to 60s for long-running programs
            )
        end_time = datetime.now()

        # Remove generated .exe file if permitted
        if COMPILED and not keep_exe:
            os.remove(output_path.with_suffix(".exe"))

        # Collect both stdout and stderr
        raw_output = (result.stdout + result.stderr).replace(": ", ":\n").strip()
        output = raw_output + f"\n[Execution Time: {(end_time - start_time).total_seconds():.2f}s]"

        return output if raw_output else None, None

    except subprocess.TimeoutExpired:
        return None, "⏱️ Execution timed out (program may be waiting for input or running too long)."
    except subprocess.CalledProcessError as e:
        return None, f"❌ Compilation or execution failed:\n{e.stderr or str(e)}"
    except:
        raise ValueError("COMPILE_CMD must not configured properly or the command is not set up on your system")

def build_title_page(lab_name: str, course: str):
    """Build the title page for a lab report."""
    return [
        Spacer(1, 2 * inch),
        Image(LOGO_PATH, width=2.5 * inch, height=2.5 * inch),
        Spacer(1, 0.5 * inch),
        Paragraph(UNIVERSITY, title_style),
        Paragraph(f"{course} — {lab_name}", subtitle_style),
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
    question = [Paragraph(f"Question {n+1}", title_style)]
    
    # Safely get the question text
    question_text = QUESTIONS[lab_index][n] if lab_index < len(QUESTIONS) and n < len(QUESTIONS[lab_index]) else None
    
    # Only add if the question exists and is not empty
    if question_text:
        question.append(Paragraph(question_text, question_style))
        question.append(Spacer(1, 0.2 * inch))
    
    src_code = list()
    with open(src_path, 'r', encoding="utf-8") as f:
        src_code.append(Preformatted(f.read(), code_style))

    # Safely get the input
    input = INPUTS[lab_index][n] if lab_index < len(INPUTS) and n < len(INPUTS[lab_index]) else None
    output, error = compile_and_run(src_path, input=input, keep_exe=KEEP_EXE)
    
    lab_outp = list()
    if output:
        lab_outp.append(Paragraph("Output", title_style))
        lab_outp.append(terminal_block(output, input))
    elif output is None:
        pass
    else:
        lab_outp.append(Paragraph("Error", title_style))
        lab_outp.append(terminal_block(error))
    lab_outp.append(Spacer(1, 0.3 * inch))

    # This will separate questions into different pages if KEEP_TOGETHER is set to True
    block = list()
    if not keep_together:
        block = [KeepTogether(question)] + src_code
    else:
        block = [KeepTogether(question + src_code)]

    return block + [KeepTogether(lab_outp)]

# ---------- MAIN ----------
for lab_index, lab_name in enumerate(PROCESS):
    lab_path = Path(f"./{lab_name}")
    lab_path.mkdir(parents=True, exist_ok=True)
    pdf_path = lab_path / f"{ROLL_NO}_{lab_name.replace(" ","")}.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)
    content = build_title_page(lab_name, COURSE)

    files = sorted(
        lab_path.glob(f"*.{EXTENSION}"), 
        key=lambda p: [
            int(x) if x.isdigit() else x.lower()
            for x in re.split(r"(\d+)", p.stem)
        ]
    )
    for q_index, src_path in enumerate(files):
        content.extend(build_question_block(lab_index, q_index, src_path, KEEP_TOGETHER))

    doc.build(content)
    print(f"✅ PDF of {lab_name} created successfully: {pdf_path}")
