from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from pathlib import Path
import base64
from fastapi.responses import FileResponse
import json
import os

app = FastAPI()

# Security settings
API_KEY_NAME = "X-API-Key"
API_KEY_HEADER = APIKeyHeader(name=API_KEY_NAME)
JOBS_DIR = "/tmp/nvflare/jobs-storage"
API_KEYS_FILE = "api_keys.json"

def load_api_keys():
   if os.path.exists(API_KEYS_FILE):
       with open(API_KEYS_FILE, 'r') as f:
           return json.load(f)
   return {}

async def verify_api_key(api_key: str = Security(API_KEY_HEADER)):
   api_keys = load_api_keys()
   if api_key in api_keys:
       return api_key
   raise HTTPException(status_code=403, detail="Invalid API key")

@app.get("/jobs/{job_id}/download")
async def download_job(
   job_id: str, 
   api_key: str = Depends(verify_api_key)
):
   job_path = Path(JOBS_DIR) / job_id
   workspace_file = job_path / "workspace"
   
   if not workspace_file.exists():
       raise HTTPException(status_code=404, detail="Workspace not found")
   
   try:
       # Read workspace as bytes (it's already a zip)
       with open(workspace_file, 'rb') as f:
           zip_bytes = f.read()
           
       # Convert to base64 for transfer
       b64_data = base64.b64encode(zip_bytes).decode('ascii')
       
       return {
           "status": "success",
           "data": b64_data,
           "job_id": job_id
       }

   except Exception as e:
       raise HTTPException(status_code=500, detail=str(e))

@app.get("/jobs/{job_id}/download/zip")
async def download_job_zip(
   job_id: str,
   api_key: str = Depends(verify_api_key)
):
   job_path = Path(JOBS_DIR) / job_id
   workspace_file = job_path / "workspace"
   
   if not workspace_file.exists():
       raise HTTPException(status_code=404, detail="Workspace not found")
   
   return FileResponse(
       path=workspace_file,
       filename=f"workspace_{job_id}.zip",
       media_type='application/zip'
   )