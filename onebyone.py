import os
import pdfkit
from PyPDF2 import PdfMerger

# Paths to directories and files
base_path = r"C:\Users\Documents"  #CHANGE THIS TO THE DIRECTORY OF THE EBOOK/TEXTBOOK
content_path = os.path.join(base_path, "content")  # Folder with HTML files
output_pdf = os.path.join(base_path, "output_textbook.pdf")  # Final merged PDF path
temp_pdf_folder = os.path.join(base_path, "temp_pdfs")  # Temporary folder for individual PDFs

# Configuration for wkhtmltopdf
config = pdfkit.configuration(wkhtmltopdf=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe") 
pdf_options = {
    "enable-local-file-access": None,
    "page-size": "A4",
    "encoding": "UTF-8",
    "margin-top": "10mm",
    "margin-bottom": "10mm",
    "margin-left": "10mm",
    "margin-right": "10mm",
}

# Create temporary folder for PDFs
os.makedirs(temp_pdf_folder, exist_ok=True)

def convert_html_to_individual_pdfs():
    html_files = sorted(
        [os.path.join(content_path, f) for f in os.listdir(content_path) if f.endswith(".html")]
    )
    
    if not html_files:
        raise FileNotFoundError("No HTML files found in the specified folder.")
    
    pdf_files = []
    for html_file in html_files:
        # Define output path for each individual PDF
        pdf_file = os.path.join(temp_pdf_folder, os.path.basename(html_file).replace(".html", ".pdf"))
        
        try:
            print(f"Converting {html_file} to {pdf_file}...")
            pdfkit.from_file(html_file, pdf_file, configuration=config, options=pdf_options)
            pdf_files.append(pdf_file)
        except Exception as e:
            print(f"Failed to convert {html_file}: {e}")
    
    return pdf_files

def merge_individual_pdfs(pdf_files):
    merger = PdfMerger()
    for pdf_file in pdf_files:
        print(f"Adding {pdf_file} to final PDF...")
        merger.append(pdf_file)
    
    merger.write(output_pdf)
    merger.close()
    print(f"Final PDF created at: {output_pdf}")

if __name__ == "__main__":
    try:
        # Step 1: Convert HTML files to individual PDFs
        individual_pdfs = convert_html_to_individual_pdfs()
        
        # Step 2: Merge individual PDFs into one
        merge_individual_pdfs(individual_pdfs)
        
        print("Process completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
