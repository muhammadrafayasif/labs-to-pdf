# 📄 C++ to PDF Converter

A simple Python tool that **automatically collects all C++ source files** in a directory, merges them into a **single, well-formatted PDF**,perfect for **assignment submissions** or **documentation**.

---

## 🚀 Features

- 🔍 Recursively finds all `.cpp` files  
- 🧩 Merges all source code into a single document
- 📚 Exports everything into a clean, submission-ready PDF  

---

## 🧰 Requirements

- **Python 3**
- **pip** for installing dependencies

### Clone the repository
```bash
git clone https://github.com/muhammadrafayasif/labs_to_pdf.git
cd labs_to_pdf
```

### Install dependencies
```bash
pip install reportlab datetime
```

## 💡 Usage
Firstly, make sure the project structure looks like this
```
folder/
│
├── Lab 1/
├───── q1.cpp
├───── q2.cpp
├── Lab 2/
├───── q1.cpp
├───── q2.cpp
├── make_pdfs.py
├── logo.png
```
Now make sure to change all necessary variables in `make_pdfs.py` according to your desire.
```python
LOGO_PATH = "./logo.png" # University Logo to be added to the title page
PROCESS = ['Lab 1'] # Add folder names (LABS) to be processed
UNIVERSITY='NED University of Engineering and Technology'
NAME = "NAME"
ROLL_NO = "CT-24000"
DEPARTMENT = "Department of Computer Science and Information Technology"
DEGREE = "Bachelor of Science (BS)"
```
Finally, run the `make_pdfs.py` script and it will automatically place PDFs in each Lab folder.
```bash
python make_pdfs.py
```

## 📝 Results
At each lab folder, you will notice a new PDF such as `CT-24000.pdf`, this is what the title page looks like.

<img width="373" height="481" alt="Cover" src="https://github.com/user-attachments/assets/5085475f-d66b-4e8b-88e6-4107f909654e" />
<img width="373" height="481" alt="Page 1" src="https://github.com/user-attachments/assets/f6488c95-365a-4d76-8387-d8ba74f2424e" />
