from fastapi import APIRouter, Request, File, UploadFile, Depends
from fastapi.responses import RedirectResponse
from app.clients.r2 import s3_client
from app.clients.supabase import supabase
from app.core import config
import uuid

router = APIRouter(prefix="/files", tags=["Files"])

@router.post("/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...)
):
    file_content = await file.read()
    file_size = len(file_content)
    file_uuid = str(uuid.uuid4())
    file_key = f"{file_uuid}_{file.filename}"
    
    s3_client.put_object(
        Bucket=config.BUCKET_NAME,
        Key=file_key,
        Body=file_content,
        ContentType=file.content_type  
    )
    
    file_url = f"{config.FILE_BASE_URL}/{file_key}"

    supabase.table('files').insert({
        "id":file.id,
        "user_id": str(uuid.uuid4()), # Placeholder Replace with actual logged-in user UUID after auth is added 
        "filename": file.filename,
        "file_key": file_key,
        "file_url": file_url,
        "content_type": file.content_type,
        "size": file_size
    }).execute()

    return RedirectResponse(url="/", status_code=303)