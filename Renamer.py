import os  
import re  
from pdfminer.high_level import extract_pages  
from pdfminer.layout import LTTextContainer, LTChar  
  
def extract_main_topic(pdf_path):  
    largest_text = ""  
    largest_font_size = 0  
  
    for page_layout in extract_pages(pdf_path):  
        for element in page_layout:  
            if isinstance(element, LTTextContainer):  
                for text_line in element:  
                    if isinstance(text_line, LTTextContainer):  
                        for character in text_line:  
                            if isinstance(character, LTChar):  
                                font_size = character.size  
                                if font_size > largest_font_size:  
                                    largest_font_size = font_size  
                                    largest_text = text_line.get_text().strip()  
    return largest_text  
  
def sanitize_filename(filename):  
    # Replace any character that is not alphanumeric, space, or allowed punctuation with an underscore  
    sanitized = re.sub(r'[^\w\s-]', '_', filename)  
    # Replace spaces with underscores  
    sanitized = re.sub(r'\s+', '_', sanitized)  
    return sanitized  
  
def get_unique_filename(directory, filename):  
    base, extension = os.path.splitext(filename)  
    counter = 1  
    new_filename = filename  
    while os.path.exists(os.path.join(directory, new_filename)):  
        new_filename = f"{base}_{counter}{extension}"  
        counter += 1  
    return new_filename  
  
def rename_pdfs_in_directory(directory):  
    for filename in os.listdir(directory):  
        if filename.lower().endswith('.pdf'):  
            pdf_path = os.path.join(directory, filename)  
            main_topic = extract_main_topic(pdf_path)  
            if main_topic:  
                sanitized_topic = sanitize_filename(main_topic)  
                new_filename = f"{sanitized_topic}.pdf"  
                new_filename = get_unique_filename(directory, new_filename)  
                new_path = os.path.join(directory, new_filename)  
                os.rename(pdf_path, new_path)  
                print(f"Renamed '{filename}' to '{new_filename}'")  
  
if __name__ == "__main__":  
    script_directory = os.path.dirname(os.path.abspath(__file__))  
    rename_pdfs_in_directory(script_directory)  
