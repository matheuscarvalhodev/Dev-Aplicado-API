from typing import List, Optional

from fastapi import (APIRouter, Depends, FastAPI, File, HTTPException, Request,
                     UploadFile)
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
# from fastapi import APIRouter, Depends, HTTPException, Query, Request
# from fastapi.responses import JSONResponse, RedirectResponse
# from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from project.app.auth.utils import obter_usuario_logado
from project.app.db import get_session, pd_engine
from project.app.models import Usuario
from project.app.utils.generate import namefile, read_xlsx

# from starlette.templating import _TemplateResponse

# from project.app.settings import settings



router = APIRouter(prefix="/uploads")

@router.post("/df", tags=["Arquivos"])
async def create_upload_file(file: UploadFile = File(...),
    # user: Usuario=Depends(obter_usuario_logado)
    ):
    if(file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" and file.filename.split(".")[-1] != "xlsx"):
        raise HTTPException(status_code=415, detail="Formato de arquivo não aceito")
    contents = await file.read()
    df = read_xlsx(contents)
    df['Data'] = df.Data.astype('datetime64[ns]')
    df = df[['Data','Nivel_agua']].fillna(0)
    df = df.rename(columns={'Data': 'data', 'Nivel_agua': 'nivel_agua'})
    try:
        await df.to_sql('DadosHistoricos', con=pd_engine)
    except Exception:
        raise HTTPException(status_code=500, detail="Falha ao processar dados")
    return JSONResponse({"message": "Dados processados"})
    # return {"filename": file.filename}

@router.post("/file", tags=["Arquivos"])
async def create_upload_file(file: UploadFile = File(...)):
    print(namefile())
    return {"filename": file.filename}

@router.post("/files", tags=["Arquivos"])
async def create_upload_files(files: List[UploadFile] = File(description="Multiple files as UploadFile"),):
    return {"filenames": [file.filename for file in files]}
