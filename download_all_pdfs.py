import requests
import os
import sys
import glob
from typing import List


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


dir: str = os.getcwd()
documents_folder: str = os.path.join(dir, 'MUSC255_Etude_LangChain/documents')
existing_documents: List[str] = glob.glob(f'{documents_folder}/*')
existing_ids: List[int] = []

for document_path in existing_documents:
    base_name: str = os.path.splitext(os.path.basename(document_path))[0]
    existing_id: int = int(''.join([char for char in base_name if char.isnumeric()]))
    existing_ids += [existing_id]

remaining_ids: List[int] = [i for i in range(1001, 1883) if i not in existing_ids]
total_to_download: int = len(remaining_ids)

for count, id in enumerate(remaining_ids):

    try:
        response = requests.get(
                f'https://digitalcommons.gardner-webb.edu/cgi/viewcontent.cgi?article={id}&context=etude'
            )
        
        with open(f'{documents_folder}/document{id}.pdf', 'wb') as f:
            f.write(response.content)
        
        update_progress((count+1) / total_to_download)

    except Exception as e:
        print(e)