from pydantic import BaseModel
from fastapi import Form
from uuid import UUID

class UserCreate(BaseModel):
    id: int
    user_id: UUID
    filename: str
    file_key: str
    file_url: str
    content_type: str
    size: int

    @classmethod
    def as_form(
        cls,
        id: int = Form(...),
        user_id: UUID = Form(...),
        filename: str = Form(...),
        file_key: str = Form(...),
        file_url: str = Form(...),
        content_type: str = Form(...),
        size: int = Form(...)
    ):
        return cls(
            id=id,
            user_id=user_id,
            filename=filename,
            file_key=file_key,
            file_url=file_url,
            content_type=content_type,
            size=size
        )