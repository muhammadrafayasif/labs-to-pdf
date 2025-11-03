import subprocess
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Preformatted, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
from pathlib import Path

# ---------- CONFIGURATION ----------
EXTENSION = "cpp"
LOGO_PATH = "./logo.png"
PROCESS = ["Lab 1"]
COMPILE_TEMPLATE = ["g++", "{0}", "-o", "{1}"]
INPUTS = [
    ["2 2\n1 3 2 4\n", "2 3\n3.2 3.7 4\n2.3 4 3.2\n", "1\n5\n1\n2\n1\n5\n2\n3\n", "5\n2 13 16 23 35\n16\n", "2 2\n2 5 10 15\n5\n"]
]

UNIVERSITY = "NED University of Engineering and Technology"
NAME = "Muhammad Raza"
ROLL_NO = "CT-24138"
DEPARTMENT = "Department of Computer Science and Information Technology"
DEGREE = "Bachelor of Science (BS)"

# ---------- STYLES ----------
styles = getSampleStyleSheet()
title_style = ParagraphStyle("CustomTitle", parent=styles["Title"], fontSize=28, alignment=1, spaceAfter=20)
subtitle_style = ParagraphStyle("Subtitle", parent=styles["Normal"], fontSize=16, alignment=1, textColor=colors.HexColor("#333333"), spaceAfter=10)
info_style = ParagraphStyle("Info", parent=styles["Normal"], alignment=1, fontSize=12, textColor=colors.HexColor("#555555"))
code_style = ParagraphStyle("CodeStyle", fontName="Courier", fontSize=9, leading=12, backColor=colors.whitesmoke, borderPadding=(5, 5, 5, 5), borderColor=colors.lightgrey, borderWidth=0.5)
terminal_style = ParagraphStyle("TerminalStyle", fontName="Courier", fontSize=9, leading=12, backColor=colors.black, textColor=colors.white, borderPadding=(5, 5, 5, 5), borderColor=colors.lightgrey, borderWidth=0.5)
heading_style = styles["Heading2"]

# ---------- HELPERS ----------
def terminal_block(text):
    pre = Preformatted(text, terminal_style)
    table = Table([[pre]])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.black),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.whitesmoke),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("INNERPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table

def compile_and_run(file_path, input_data):
    COMPILE_CODE = [s.format(file_path, file_path.with_suffix("")) for s in COMPILE_TEMPLATE]
    try:
        start_time = datetime.now()
        subprocess.run(COMPILE_CODE, check=True)
        result = subprocess.run([file_path.with_suffix("")], input=input_data, capture_output=True, text=True)
        end_time = datetime.now()

        output = result.stdout.replace(": ", ":\n").strip()
        output += f"\n\n[INPUT(S) PROVIDED]\n{input_data}"
        output += f"\n[Execution Time: {(end_time - start_time).total_seconds():.2f}s]"
        return output, None
    except subprocess.CalledProcessError as e:
        return None, f"❌ Compilation or execution failed:\n{e.stderr or str(e)}"

def build_title_page():
    return [
        Spacer(1, 2 * inch),
        Image(LOGO_PATH, width=2.5 * inch, height=2.5 * inch),
        Spacer(1, 0.5 * inch),
        Paragraph(UNIVERSITY, title_style),
        Paragraph(f"Data Structures and Algorithms", subtitle_style),
        Spacer(1, 0.5 * inch),
        Paragraph(f"Author: {NAME}", info_style),
        Paragraph(f"Roll No: {ROLL_NO}", info_style),
        Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", info_style),
        Spacer(1, 1.9 * inch),
        Paragraph(f"{DEPARTMENT}<br/>{DEGREE}", info_style),
        PageBreak()
    ]

def build_question_block(n, file_path, input_data):
    block = [Paragraph(f"Question {n+1}", heading_style)]
    with open(file_path, 'r') as f:
        block.append(Preformatted(f.read(), code_style))

    if input_data:
        output, error = compile_and_run(file_path, input_data)
        if output:
            block.append(Paragraph("Output", heading_style))
            block.append(terminal_block(output))
        else:
            block.append(Paragraph("Error", heading_style))
            block.append(terminal_block(error))
    block.append(Spacer(1, 0.5 * inch))
    return block

# ---------- MAIN ----------
for lab_index, lab_name in enumerate(PROCESS):
    lab_path = Path(f"./{lab_name}")
    lab_path.mkdir(parents=True, exist_ok=True)
    pdf_path = lab_path / f"{ROLL_NO}_{lab_name}.pdf"
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)
    content = build_title_page()

    files = lab_path.glob(f"*.{EXTENSION}")
    for q_index, file_path in enumerate(files):
        input_data = INPUTS[lab_index][q_index] if lab_index < len(INPUTS) else ""
        content.extend(build_question_block(q_index, file_path, input_data))

    doc.build(content)
    print(f"✅ PDF of {lab_name} created successfully: {pdf_path}")
