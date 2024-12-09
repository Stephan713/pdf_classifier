from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
from PyPDF2 import PdfReader
from output_format import classify_text, ClassificationTypes
from typing import get_args

def get_text_classification(pdf_file: str):
    load_dotenv()

    pdf_folder = os.environ['PDF_FOLDER']

    pdf_file_path = Path(pdf_folder, pdf_file)

    # Load the PDF file
    reader = PdfReader(pdf_file_path)

    pdf_text = ''
    # Extract text from each page
    for page in reader.pages:
        pdf_text += page.extract_text()

    system_message = """
    You are an intelligent text classifier. 
    Your job is to categorize input text into one of the predefined categories: {OPTIONS} based on its content. 
    Consider the context, tone, keywords, and structure of the text to make your decision. 
    Provide a single category as your output, followed by a brief explanation of your reasoning.
    Also extract the effective year mentioned in the document.
    """

    user_message = """
    Classify the below text:
    
    
    {pdf_text}
    """


    OPTIONS = get_args(ClassificationTypes.__annotations__["option"])

    prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    system_message,
                ),
                (
                    "human",
                    user_message
                ),
            ]
        )

    model = ChatOpenAI(
        model="gpt-4o",
        temperature=0.0,
    )

    # # Inspecting the args_schema
    # args_schema = classify_text.args_schema
    #
    # # Extract fields and types
    # for field_name, field_type in args_schema.__annotations__.items():
    #     print(f"Argument: {field_name}, Type: {field_type}")

    model_with_tools = model.bind_tools([classify_text], tool_choice="required")

    chain = prompt_template | model_with_tools

    response = chain.invoke(
            {
                "OPTIONS": OPTIONS,
                "pdf_text": pdf_text
            }
        )

    print(response.tool_calls[0]['args'])

    if isinstance(response.tool_calls[0]['args']['classification_type'], dict):
        print(response.tool_calls[0]['args']['classification_type']['option'])
    else:
        print(response.tool_calls[0]['args']['classification_type'])

    print(response.tool_calls[0]['args']['year'])
    print(response.tool_calls[0]['args']['reason'])

    return None

if __name__ == '__main__':
    pdf_file = "AWS_certification_paths.pdf"

    get_text_classification(pdf_file)