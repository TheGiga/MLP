from typing import Optional

from pydantic import BaseModel, validator


class Title(BaseModel):
    id: int
    code: str
    names: dict
    status: dict
    announce: Optional[str]
    posters: dict
    type: dict  # {full_string, code, string, series, length}
    genres: list
    player: dict
    description: str

    class Config:
        validate_assignment = True

    @validator('announce')
    def float_validator(cls, v):
        if v is None:
            return ""
        return v

