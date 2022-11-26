from typing import List, Optional

from fastapi import APIRouter, FastAPI, File, Request, UploadFile
from fastapi.staticfiles import StaticFiles

from project.app.utils.generate import namefile

# from fastapi import APIRouter, Depends, HTTPException, Query, Request
# from fastapi.responses import JSONResponse, RedirectResponse
# from sqlalchemy import desc, select
# from sqlalchemy.ext.asyncio import AsyncSession
# from starlette.templating import _TemplateResponse

# from project.app.auth import hash_provider, token_provider
# from project.app.db import get_session
# from project.app.models import Previsao, Usuario
# from project.app.settings import settings



router = APIRouter(prefix="/uploads")

@router.post("/file", tags=["Arquivos"])
async def create_upload_file(file: UploadFile = File(...)):
    print(namefile())
    return {"filename": file.filename}

@router.post("/files", tags=["Arquivos"])
async def create_upload_files(files: List[UploadFile] = File(description="Multiple files as UploadFile"),):
    return {"filenames": [file.filename for file in files]}
