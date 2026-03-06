from dotenv import load_dotenv
import os 

load_dotenv()

R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
BUCKET_NAME=os.getenv("BUCKET_NAME")
FILE_BASE_URL=os.getenv("FILE_BASE_URL")