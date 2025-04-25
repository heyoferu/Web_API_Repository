# from fileinput import filename
# import mimetypes
# import os
# from fastapi import APIRouter, Depends, HTTPException
# from fastapi.responses import FileResponse
# from sqlmodel import select
# from db import get_session, Session
# from models import Books, Magazines, Podcasts, Tesis, Videos
# # from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# #scheme = HTTPBearer()
# # token: str = Depends(scheme)

# router = APIRouter(prefix="/content", tags=["content"])

# @router.get("/file/{file_name}")
# def get_file(file_name: str):
#     file_path = f"files/{file_name}"

#     if not os.path.isfile(file_path):
#         raise HTTPException(status_code=404, detail="Archivo no encontrado")

#     mime_type, _ = mimetypes.guess_type(file_path)
#     return FileResponse(path=file_path, filename=file_name, media_type=mime_type)
