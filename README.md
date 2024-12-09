# pdf classifier

## Setting up environment:
pip install -r requirements.txt


## Changes to run the script:

## File: .env
Create a .env file and add the below fields values.
PDF_FOLDER -> Folder from which the pdf files are to be read
OPENAI_API_KEY -> API key from Open AI.

## File: output_format.py
Line 6 -> option: Literal["Tax", "Medical", "Other"]
    Add the categories

## File: pdf_classifier.py
Line 87 -> pdf_file
    Provide the pdf file name to be classified.

