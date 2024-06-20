from datetime import datetime
from pydantic import BaseModel


class LinkBase(BaseModel):
    url: str


class LinkCreate(BaseModel):
    id: int
    url: str
    created: datetime


class Link(LinkBase):
    id: int

    class Config:
        from_attributes = True


class LinkResponse(BaseModel):
    message: str
    status: str
