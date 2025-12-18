import os
import sys
import base64
import tempfile
import glob
from openai import OpenAI
from pdf2image import convert_from_path
 

#enter API key; this code isn't meant to be ran or shown on the frontend
#replace the string with the proper environment variable fetch os.environ.get("KEY_WHERE_API_KEY_IS_BEING_STORED") if this code is public-facing
client = OpenAI(
    api_key='openai-api-key'  
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


def extract_text_from_openai_api(image_path: str):
    """
    Sends the base64-encoded image to the OpenAI API and extracts text
    """
    base64_image = encode_image(image_path)
    try:
        #yes this looks horrifying
        response = client.responses.create(
            model="gpt-5-mini",
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
 

def process_pdf(pdf_path: str, output_txt_path: str):
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
 
        text = extract_text_from_openai_api(image_path)
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

    process_pdf(pdf_path, output_txt_path)
 
 
def main_specifyinput(pdf_path: str, txt_folder_path: str=''):
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

    process_pdf(pdf_path, output_txt_path)


def main2():
    for pdf in glob.glob('documents/*'):
        main_specifyinput(pdf_path=pdf, txt_folder_path="processed-documents")


main2()