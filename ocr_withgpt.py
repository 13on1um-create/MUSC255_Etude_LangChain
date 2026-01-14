import os
import sys
import base64
import tempfile
import glob
from typing import List
from openai import OpenAI

"""
use pyvips for pdf processing if it's installed, otherwise use pdf2image. 
pyvips is excluded from requirements.txt because it requires manual setup outside of pip, but it's significantly faster and less memory-intensive than pdf2image, especially for larger PDFs.

to install pyvips:
- download the latest "vips-dev-w64-all" zip file from https://github.com/libvips/build-win64-mxe/releases 
- extract all (anywhere you want)
- add the filepath of the "bin" folder to your PATH:
    - click through the folder until you find "bin"
    - copy the (absolute) file path of the "bin" folder
    - windows search "environment variables" and click "edit the system environment varaibles" or something similar. then click on "Environment Variables"
    - find "PATH" in the "System variables" section, click "Edit", then "New", then add the file path of the "bin" folder and move it above anything with libvips or pyvips as a dependency
    - apply changes
- restart your machine
- run "pip install pyvips" in your desired python environment
"""
try:
    import pyvips
    has_pyvips = True

except ModuleNotFoundError:
    from pdf2image import convert_from_path
    has_pyvips = False

# if pyvips is installed but libvips (the library pyvips wraps around) can't be found by pyvips, attempt to manually inform pyvips of the path to libvips; if the import still fails (which it usually does), use pdf2image
except OSError:
    
    while True:
        vip_path: str = input('libvips/bin was not found in PATH. Paste the path to your libvips bin: ')

        try:
            os.add_dll_directory(vip_path)
            break
        except OSError:
            print(f'"{vip_path}" is not a valid file path.')

    try:
        import pyvips  
        has_pyvips = True
    
    except:
        import traceback
        print(f'{traceback.format_exc()}\n\n^ Error importing pyvips, will use pdf2image instead.')
        from pdf2image import convert_from_path
        has_pyvips = False


os.environ['OPENAI_API_KEY'] = input('Enter Openai API key: ')


client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY')
)


# if pdf2image is being used, it might exceed Pillow's default anti-DDOS max pixels limit for large PDFs
from PIL import Image
Image.MAX_IMAGE_PIXELS = 16000 * 16000


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
 

def process_pdf(pdf_path: str, output_txt_path: str, openai_model: str, dpi: int=300):
    """
    Converts each page of the PDF to an image, extracts text, and writes to a txt file
    """
    try:
        print("Converting PDF to images...")

        if has_pyvips:
            initial_convert = pyvips.Image.new_from_file(pdf_path)
            total_pages: int = initial_convert.get("n-pages")
            images = [pyvips.Image.new_from_file(pdf_path, dpi=dpi, page=i) for i in range(total_pages)]
        
        else:
            images = convert_from_path(pdf_path, dpi=dpi)
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

            if has_pyvips:
                image.write_to_file(image_path)
            
            else:
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

    # if a dedicated txt files folder is passed in, put txt files in that folder, otherwise put them in the same folder as the PDF
    if len(txt_folder_path) != 0:
        output_txt_path = f"{txt_folder_path}/{base_name}.txt"
    else:
        output_dir = os.path.dirname(pdf_path)
        output_txt_path = os.path.join(output_dir, f"{base_name}.txt")

    process_pdf(pdf_path, output_txt_path, openai_model=openai_model)


def main2():
    """
    For processing some or all of the documents in the documents folder excluding the ones already present in processed-documents
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
    documents_folder: str = os.path.join(dir, 'documents')
    processed_documents_folder: str = os.path.join(dir, 'processed-documents')

    processed_document_ids: List[int] = [nums_in_string(base_name(filepath)) for filepath in glob.glob(f'{processed_documents_folder}/*')]
    unprocessed_documents: List[str] = [filepath for filepath in glob.glob(f'{documents_folder}/*') if nums_in_string(base_name(filepath)) not in processed_document_ids]

    n = input(f'\nHow many documents to process? Number of remaining documents: {len(unprocessed_documents)}\n')

    try:
        n = int(n)
    except:
        return

    for index, filepath in enumerate(unprocessed_documents[:n], start=1):
        print(f'\nProcessing {filepath} (file {index}/{n})...')
        main_specifyinput(pdf_path=filepath, txt_folder_path=processed_documents_folder, openai_model='gpt-5-mini')


main2()