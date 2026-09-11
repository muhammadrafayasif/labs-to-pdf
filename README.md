# 🧾 Automated Lab Report Generator (Python + ReportLab)

This project automatically compiles, runs, and generates PDF lab reports for programming labs.  
It handles everything — from compiling C++ files to capturing output and formatting it into a professional, university-style PDF with your name, roll number, and department.

---

## 📸 Sample Output

The generated PDF includes:

- University logo and title page
- Each lab question’s source code
- Automatically captured program output (styled like a terminal)
- Execution time for each task
- Automatic date and metadata

Example PDF: [CT-24000.pdf](/Lab%201/CT-24000_Lab1.pdf)

---

## ⚙️ Features

- ✅ Automatic Compilation — Uses `g++` to compile each `.cpp` file
- 📤 Output Capture — Captures console output and formats it like a terminal
- 🖋️ Beautiful PDF Generation — Uses ReportLab for clean, styled reports
- 🧑‍🎓 Customizable Branding — Add your own logo, name, roll number, department, and degree
- 📂 Multi-Lab Support — Process multiple folders like `"Lab 1"`, `"Lab 2"`, etc.
- ⏱️ Execution Timing — Displays how long each program took to run
- 🛠️ Error Handling — Gracefully reports compilation or runtime errors

---

## 🗂️ Project Structure

```bash
📦 labs-to-pdf/
│
├── Lab 1/
│   ├── 1.cpp
│   ├── 2.cpp
│   └── ...
│
├── logo.png                # University logo for the title page
├── make_pdfs.py            # Main automation script
└── README.md
```

---

## 🧰 Requirements

You’ll need:

* Python 3.8+
* ReportLab for PDF generation

Install dependencies with:

```bash
pip install reportlab
```

---

## 🧑‍💻 Usage

1. Place your files inside folders like `Lab 1`, `Lab 2`, etc.
2. Update configuration at the top of `make_pdfs.py`:

```python
EXTENSION = "py"
# Set COMPILED to False when using interpreted languages like Python
COMPILED = False

LOGO_PATH = "./logo.png"

# The complete command for program compilation/interpretation
# Keep in mind that src_path and output_path are constants the program will replace 
# For python, replace with ["python", "output_path"]
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
```

3. Run the generator:

```bash
python make_pdfs.py
```

4. PDFs will be generated inside each lab folder individually.

---

## 🧠 Tips

* A custom font can be used, simply replace `font.ttf` with another font of your choice.
* Ensure your files compile cleanly and produce output.
* Customize fonts, colors, and layout by editing the paragraph and table styles in the script.
* Adjust the `EXECUTION_TIMEOUT` constant in the script if your programs take longer to run.

---

## 🪪 License

This project is released under the [MIT License](LICENSE).

Feel free to modify and adapt it for your institution or personal use.

---
