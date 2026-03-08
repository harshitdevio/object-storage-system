import uuid
from app.clients.r2 import s3_client
from app.core import config

async def upload_to_r2(file_content: bytes, filename: str, content_type: str) -> dict:
    file_uuid = str(uuid.uuid4())
    file_key = f"{file_uuid}_{filename}"

    s3_client.put_object(
        Bucket=config.BUCKET_NAME,
        Key=file_key,
        Body=file_content,
        ContentType=content_type
    )

    file_url = f"{config.FILE_BASE_URL}/{file_key}"

    return {
        "file_key": file_key,
        "file_url": file_url,
        "size": len(file_content)
    }