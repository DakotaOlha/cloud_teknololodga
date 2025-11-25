from fastapi import APIRouter, UploadFile, File, HTTPException
from storage import StorageService

router = APIRouter(prefix="/storage", tags=["Azure Blob Storage"])
service = StorageService()


@router.post("/files")
async def upload_file(file: UploadFile = File(...)):
    try:
        filename = service.upload_file(file)
        return {"message": f"File '{filename}' successfully uploaded to Azure Blob Storage."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/files")
async def list_files():
    try:
        return {"files": service.list_files()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/files/{filename}")
async def download_file(filename: str):
    try:
        content = service.download_file(filename)
        return {"filename": filename, "content": content}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/files/{filename}")
async def delete_file(filename: str):
    try:
        service.delete_file(filename)
        return {"message": f"File '{filename}' successfully deleted from Azure Blob Storage."}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))