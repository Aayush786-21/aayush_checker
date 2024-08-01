from flask import Flask, request, render_template, redirect, url_for
import PyPDF2

app = Flask(__name__)

# List of required sections
REQUIRED_SECTIONS = [
    "Introduction",
    "Problem Statement",
    "Objectives",
    "Methodology",
    "Requirement Identification",
    "Study of Existing System",
    "Literature Review",
    "Requirement Analysis",
    "Feasibility Study",
    "Technical Feasibility",
    "Operational Feasibility",
    "Economic Feasibility",
    "High-Level Design of System",
    "Flow Chart",
    "Working Mechanism of Proposed System",
    "Description of Algorithms",
    "Gantt Chart",
    "Expected Outcome",
    "References"
]

def check_pdf_sections(file_stream):
    reader = PyPDF2.PdfReader(file_stream)
    content = []
    for page in reader.pages:
        content.append(page.extract_text())
    content = '\n'.join(content).lower()  # Convert content to lowercase

    # Check for each required section in the content
    missing_sections = [section for section in REQUIRED_SECTIONS if section.lower() not in content]
    return missing_sections

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser also submits an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and file.filename.endswith('.pdf'):
            missing_sections = check_pdf_sections(file)
            return render_template('result.html', missing_sections=missing_sections)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
