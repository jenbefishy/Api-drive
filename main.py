from fastapi import FastAPI, UploadFile, File
from drive import search_file, download_file, list_files, delete_file, upload_file
from credentials import get_creds


app = FastAPI()

creds = get_creds()


@app.get("/")
async def list():
    return list_files()


@app.get("/search")
async def search(file_name: str):
    return search_file(file_name)


@app.get("/download")
async def download(file_id: str | None = None, file_name: str | None = None):
    content = download_file(file_id, file_name)
    if content:
        return {"file_content": content.decode('utf-8')}
    return {"error": "File not found or couldn't be downloaded"}


@app.get("/delete")
async def delete(file_id: str | None = None, file_name: str | None = None):
    success = delete_file(file_id, file_name)
    if success:
        return {"status": "File deleted successfully"}
    return {"error": "File not found or couldn't be deleted"}


@app.post("/upload")
async def upload(file: UploadFile = File(...), parent_folder_id: str | None = None):
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    mime_type = file.content_type
    file_id = upload_file(file.filename, file_path, mime_type, parent_folder_id)

    if file_id:
        return {"status": "File uploaded successfully", "file_id": file_id}
    return {"error": "File couldn't be uploaded"}
