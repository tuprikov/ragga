import pdfplumber


def extract_pdf_text(file_path):
    """
    Extracts text from a PDF file.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        dict: A dictionary with page numbers as keys and extracted text as values.
    """
    extracted_data = {}

    try:
        # Open the PDF file
        with pdfplumber.open(file_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                # Extract text from each page
                text = page.extract_text()
                if text:  # Only save pages with actual content
                    extracted_data[page_number] = text.strip()

    except Exception as e:
        print(f"An error occurred while processing the PDF: {e}")

    return extracted_data


def save_extracted_text_to_file(extracted_data, output_path):
    """
    Saves extracted text to a plain text file.

    Args:
        extracted_data (dict): Extracted text data from the PDF.
        output_path (str): Path to save the plain text file.
    """
    try:
        with open(output_path, "w", encoding="utf-8") as file:
            for _, text in extracted_data.items():
                file.write(text + "\n")
        print(f"Extracted text has been saved to {output_path}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")
