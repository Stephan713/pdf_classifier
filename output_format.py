from langchain_core.tools import tool
from pydantic import BaseModel
from typing import Literal

class ClassificationTypes(BaseModel):
    option: Literal["Tax", "Medical", "Other"]

class ClassificationSchema(BaseModel):
    classification_type: ClassificationTypes = "The class the document belongs to. The default type is Other, if the document doesnt belong to the listed types."
    year: str = "Year effective in the text. If there is no year in the text, default to 'NA'"
    reason: str = "The reason for the classification."

@tool("classify_text", args_schema=ClassificationSchema)
def classify_text():
    """ Classify the given text into different types."""
    return None