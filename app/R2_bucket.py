import boto3
from botocore.config import Config
from fastapi import APIRouter, Request, Form, File, UploadFile, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from app.clients.supabase import supabase
from app.core import config


router = APIRouter()
templates = Jinja2Templates(directory="./employee_repo/templates")

s3_client = boto3.client(
    service_name="s3",
    endpoint_url=f"https://{config.R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
    aws_access_key_id=config.R2_ACCESS_KEY_ID,
    aws_secret_access_key=config.R2_SECRET_ACCESS_KEY,
    region_name="auto",  
    config=Config(signature_version="s3v4"),
)

class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    salary: float

    @classmethod
    def as_form(
        cls,
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(...),
        salary: float = Form(...)
    ):
        return cls(first_name=first_name, last_name=last_name, email=email, salary=salary)

@router.post("/add")
async def add_employee(
    request: Request,
    employee: EmployeeCreate = Depends(EmployeeCreate.as_form),
    image: UploadFile = File(None)
):
    image_url = None
    
    if image and image.filename != "":
        image_filename = f"{employee.first_name}_{employee.last_name}_{image.filename}"
        file_content = await image.read()
        
        s3_client.put_object(
            Bucket=config.BUCKET_NAME,
            Key=image_filename,
            Body=file_content,
            ContentType=image.content_type  
        )
        
        image_url = f"{config.FILE_BASE_URL}/{image_filename}"

    supabase.table('employees').insert({
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'email': employee.email,
        'salary': employee.salary,
        'image_url': image_url
    }).execute()

    return RedirectResponse(url="/", status_code=303)