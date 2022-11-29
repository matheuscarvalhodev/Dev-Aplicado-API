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
from project.app.db import get_session
from project.app.models import DadosHistoricos, Usuario, UsuarioSignin
from project.app.utils.generate import namefile, read_xlsx

# from starlette.templating import _TemplateResponse

# from project.app.settings import settings



router = APIRouter(prefix="/uploads")

@router.post("/df", tags=["Arquivos"], summary=["Upload dos dados de previsão"])
async def create_upload_file(file: UploadFile = File(...),
    user: Usuario=Depends(obter_usuario_logado),
    session: AsyncSession = Depends(get_session)
    ):
    if(file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" and file.filename.split(".")[-1] != "xlsx"):
        raise HTTPException(status_code=415, detail="Formato de arquivo não aceito")
    contents = await file.read()
    df = read_xlsx(contents)
    df['Data'] = df.Data.astype('datetime64[ns]')
    df = df[['Data','Nivel_agua']].fillna(0)
    df = df.rename(columns={'Data': 'data', 'Nivel_agua': 'nivel_agua'})
    if(user.tipo_usuario >= 2):
        try:
            for i in df.itertuples():
                _dados_historicos = DadosHistoricos(data=i[1], nivel_agua=i[2])
                session.add(_dados_historicos)
            await session.commit()
        except Exception:
            raise HTTPException(status_code=500, detail="Falha ao processar dados")
        return JSONResponse({"message": "Dados processados"})
    raise HTTPException(status_code=401, detail="Usuário não autorizado")

@router.post("/file", tags=["Arquivos"], summary=['Upload de apenas um arquivo'])
async def create_upload_file(file: UploadFile = File(...), ):
    print(namefile())
    return {"filename": file.filename}

@router.post("/files", tags=["Arquivos"], summary=["Upload de mais de um arquivo"])
async def create_upload_files(files: List[UploadFile] = File(description="Multiple files as UploadFile"),):
    return {"filenames": [file.filename for file in files]}
