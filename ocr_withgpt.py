import os
import sys
import base64
import tempfile
import glob
from typing import List
from openai import OpenAI
from pdf2image import convert_from_path
 

os.environ['OPENAI_API_KEY'] = input('Enter Openai API key: ')


client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY')
) 


def update_progress(progress: float):
    assert 0 <= progress <= 1, "progress must be a decimal between 0 (incomplete) and 1 (complete)"
    """
    Prints a simple loading bar in the terminal to keep track of progress
    """
    bar_length = 50
    block = int(round(bar_length * progress))
    text = f"\rProgress: [{'#' * block + '-' * (bar_length - block)}] {round(progress * 100, 2)}%"
    sys.stdout.write(text)
    sys.stdout.flush()


def encode_image(image_path: str):
    """
    Encodes an image file to a base64 string
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def extract_text_from_openai_api(image_path: str, openai_model: str):
    """
    Sends the base64-encoded image to the OpenAI API and extracts text
    """
    base64_image = encode_image(image_path)
    try:
        #yes this looks horrifying
        response = client.responses.create(
            model=openai_model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text",
                         "text": "Extract the text from this image, ensuring all text is captured accurately. Do not include any markdown or code formatting. Describe non-textual images accurately and in detail."},
                        {"type": "input_image",
                         "image_url": f"data:image/jpeg;base64,{base64_image}"},
                    ],
                }
            ],
        )
        return response.output_text
    except Exception as e:
        print(f"\nError extracting text from image {image_path}: {e}")
        return ""
 

def process_pdf(pdf_path: str, output_txt_path: str, openai_model: str):
    """
    Converts each page of the PDF to an image, extracts text, and writes to a txt file
    """
    try:
        print("Converting PDF to images...")
        images = convert_from_path(pdf_path, dpi=500)
        total_pages = len(images)
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return
 
    extracted_text = []
 
    print("Extracting text from images...")
    update_progress(0)
    for current_page_num, image in enumerate(images, start=1):
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_image:
            image_path = temp_image.name
            image.save(image_path, "JPEG")
 
        text = extract_text_from_openai_api(image_path=image_path, openai_model=openai_model)
        extracted_text.append(text)
 
        #remove the temporary image file
        os.remove(image_path)
 
        #update progress
        update_progress(current_page_num / total_pages)
 
    #write all extracted text to an output txt file
    try:
        with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write("\n".join(extracted_text))
        print(f"\nText extraction complete. Output saved to: {output_txt_path}")
    except Exception as e:
        print(f"\nError writing to txt file: {e}")
 

def main():
    """
    For running main() via terminal input
    """
    pdf_path = input('Enter the full path to the PDF file: ').strip()
 
    if not os.path.isfile(pdf_path):
        print(f'The path "{pdf_path}" does not exist or is not a file.')
        return
 
    if not pdf_path.lower().endswith('.pdf'):
        print("The provided file is not a PDF.")
        return
 
    #defines txt file path as in the same region and having the same name as the pdf 
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_dir = os.path.dirname(pdf_path)
    output_txt_path = os.path.join(output_dir, f"{base_name}.txt")

    process_pdf(pdf_path, output_txt_path, openai_model='gpt-5-mini')
 
 
def main_specifyinput(pdf_path: str, txt_folder_path: str='', openai_model: str='gpt-5-mini'):
    """
    For running main() via code instead of terminal input
    """

    if not os.path.isfile(pdf_path):
        print(f'The path "{pdf_path}" does not exist or is not a file.')
        return
 
    if not pdf_path.lower().endswith('.pdf'):
        print("The provided file is not a PDF.")
        return
    
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    if len(txt_folder_path) != 0:
        output_txt_path = f"{txt_folder_path}/{base_name}.txt"
    else:
        output_dir = os.path.dirname(pdf_path)
        output_txt_path = os.path.join(output_dir, f"{base_name}.txt")

    process_pdf(pdf_path, output_txt_path, openai_model=openai_model)


def main2():
    """
    For processing all the documents in the documents folder excluding the ones already present in processed-documents
    """

    def nums_in_string(string: str) -> int:
        """
        Returns all the numbers in the passed string concatenated into an integer
        """
        return int(''.join([char for char in string if char.isnumeric()]))
    
    def base_name(filepath: str) -> str:
        """
        Returns the name of the file in the filepath without all the folders preceding it
        """
        return os.path.splitext(os.path.basename(filepath))[0]
    
    dir = os.getcwd()
    documents_folder: str = os.path.join(dir, 'MUSC255_Etude_LangChain/documents')
    processed_documents_folder: str = os.path.join(dir, 'MUSC255_Etude_LangChain/processed-documents')

    processed_document_ids: List[int] = [nums_in_string(base_name(filepath)) for filepath in glob.glob(f'{processed_documents_folder}/*')]
    unprocessed_documents: List[str] = [filepath for filepath in glob.glob(f'{documents_folder}/*') if nums_in_string(base_name(filepath)) not in processed_document_ids]

    for filepath in unprocessed_documents[:20]:
        main_specifyinput(pdf_path=filepath, txt_folder_path=processed_documents_folder, openai_model='gpt-4o-mini')


main2()