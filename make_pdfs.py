EXTENSION = "cpp"
LOGO_PATH = "./logo.png" # University Logo to be added to the title page
PROCESS = ["Lab 1"] # Add folder names (LABS) to be processed
COMPILE_TEMPLATE = ["g++", "{0}", "-o", "{1}"] # Compilation code to run task

# FORMAT = [ [FIRST LAB INPUTS], [SECOND LAB INPUTS], ... ]
INPUTS = [ 
    ["2 2\n1 3 2 4\n", "2 3\n3.2 3.7 4\n2.3 4 3.2\n", "1\n5\n1\n2\n1\n5\n2\n3\n", "5\n2 13 16 23 35\n16\n", "2 2\n2 5 10 15\n5\n"] 
] # User input for each lab task

UNIVERSITY="NED University of Engineering and Technology"
NAME = "NAME"
ROLL_NO = "CT-24000"
DEPARTMENT = "Department of Computer Science and Information Technology"
DEGREE = "Bachelor of Science (BS)"

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

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "CustomTitle",
    parent=styles["Title"],
    fontSize=28,
    alignment=1,  # center
    spaceAfter=20,
)

subtitle_style = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontSize=16,
    alignment=1,
    textColor=colors.HexColor("#333333"),
    spaceAfter=10,
)

info_style = ParagraphStyle(
    "Info",
    parent=styles["Normal"],
    alignment=1,
    fontSize=12,
    textColor=colors.HexColor("#555555"),
)

code_style = ParagraphStyle(
    "CodeStyle",
    fontName="Courier",
    fontSize=9,
    leading=12,
    backColor=colors.whitesmoke,
    borderPadding=(5, 5, 5, 5),
    borderColor=colors.lightgrey,
    borderWidth=0.5,
)

terminal_style = ParagraphStyle(
    "TerminalStyle",
    fontName="Courier",
    fontSize=9,
    leading=12,
    backColor=colors.black,
    textColor=colors.white,
    borderPadding=(5, 5, 5, 5),
    borderColor=colors.lightgrey,
    borderWidth=0.5,
)

heading_style = styles["Heading2"]
body_style = styles["BodyText"]

for LAB_NUMBER, _ in enumerate(PROCESS):
    pdf_path = f"./{_}/{ROLL_NO}.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)

    lab = []

    # ---------- TITLE PAGE ----------
    lab.append(Spacer(1, 2 * inch))

    # University Logo (centered)
    lab.append(Image(LOGO_PATH, width=2.5 * inch, height=2.5 * inch))
    lab.append(Spacer(1, 0.5 * inch))

    # Title and Subtitle
    lab.append(Paragraph(UNIVERSITY, title_style))
    lab.append(Paragraph(f"Data Structures and Algorithms - {_}", subtitle_style))
    lab.append(Spacer(1, 0.5 * inch))

    # Author and Date
    lab.append(Paragraph(f"Author: {NAME}", info_style))
    lab.append(Paragraph(f"Roll No: {ROLL_NO}", info_style))
    lab.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", info_style))
    lab.append(Spacer(1, 1.9 * inch))

    # Footer note or department info
    lab.append(Paragraph(
        f"{DEPARTMENT}<br/>{DEGREE}",
        info_style
    ))
    lab.append(PageBreak())

    files = Path(f'./{_}').glob(f'*.{EXTENSION}')
    for n, i in enumerate(files):
        INPUT = INPUTS[LAB_NUMBER][n]
        if INPUT:
            COMPILE_CODE = [s.format(i, i.with_suffix("")) for s in COMPILE_TEMPLATE]
            subprocess.run(COMPILE_CODE, check=True)
            RESULT = subprocess.run([i.with_suffix("")], input=INPUT, capture_output=True, text=True)
            OUTPUT = RESULT.stdout.replace(": ", ":\n").strip()
            OUTPUT += "\n\n[INPUT(S) PROVIDED]\n" + INPUT
        with open(f'./{i}', 'r') as f:
            lab.append(Paragraph(f"Question {n+1}", heading_style))
            lab.append(Preformatted(f.read(), code_style))
            if INPUT:
                lab.append(Paragraph(f"Output", heading_style))
                lab.append(terminal_block(OUTPUT))
            lab.append(Spacer(1, 0.5 * inch))

    doc.build(lab)

    print(f"✅ PDF of {_} created successfully: {pdf_path}")
