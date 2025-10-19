LOGO_PATH = "./logo.png" # University Logo to be added to the title page
PROCESS = ['Lab 1'] # Add folder names (LABS) to be processed
UNIVERSITY='NED University of Engineering and Technology'
NAME = "NAME"
ROLL_NO = "CT-24000"
DEPARTMENT = "Department of Computer Science and Information Technology"
DEGREE = "Bachelor of Science (BS)"

import glob
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime

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

heading_style = styles["Heading2"]
body_style = styles["BodyText"]

for _ in PROCESS:
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

    files = glob.glob(f'./{_}/*.cpp')
    for n, i in enumerate(files):
        with open(f'./{i}', 'r') as f:
            lab.append(Paragraph(f"Question {n+1}", heading_style))

            lab.append(Preformatted(f.read(), code_style))
            lab.append(Spacer(1, 0.5 * inch))

    doc.build(lab)

    print(f"✅ PDF of {_} created successfully: {pdf_path}")
