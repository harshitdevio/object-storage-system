from fastapi import APIRouter, Request, File, UploadFile, Depends
from fastapi.responses import RedirectResponse
from service.database_service import save_file_metadata
from service.bucket_storage import upload_to_r2

router = APIRouter(prefix="/files", tags=["Files"])

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_content = await file.read()
    file_size = len(file_content)

    file_key, file_url = await upload_to_r2(
        file_content,
        file.filename,
        file.content_type
    )

    await save_file_metadata(
        file.filename,
        file_key,
        file_url,
        file.content_type,
        file_size
    )

    return RedirectResponse(url="/", status_code=303)