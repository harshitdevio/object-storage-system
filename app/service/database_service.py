import uuid
from app.clients.supabase import supabase

async def save_file_metadata(filename, file_key, file_url, content_type, size):
    supabase.table("files").insert({
        "id": str(uuid.uuid4()),
        "user_id": str(uuid.uuid4()),  # to be replaced later with auth user
        "filename": filename,
        "file_key": file_key,
        "file_url": file_url,
        "content_type": content_type,
        "size": size
    }).execute()