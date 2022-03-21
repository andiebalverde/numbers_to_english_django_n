from pydantic import BaseModel

class NumToEnglishRequest(BaseModel):
    number: int

class NumToEnglishResponse(BaseModel):
    status: str
    num_in_english: str
