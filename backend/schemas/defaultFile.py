from typing import Optional
from pydantic import BaseModel, Field
from typing_extensions import Annotated


class Message(BaseModel):
    message: str
