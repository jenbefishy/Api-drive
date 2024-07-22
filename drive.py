import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

from credentials import get_creds


def get_drive_service():
    creds = get_creds()
    return build('drive', 'v3', credentials=creds)


def list_files():
    service = get_drive_service()
    results = service.files().list().execute()
    return results.get('files', [])


def search_file(file_name):
    service = get_drive_service()
    query = f'name="{file_name}"'
    results = service.files().list(q=query).execute()

    if not results:
        return False

    return results.get('files', [])


def download_file(file_id=None, file_name=None):
    if file_id:
        return download_file_by_id(file_id)
    elif file_name:
        files = search_file(file_name)
        if not files:
            print(f"Could not find file {file_name}")
            return None
        if len(files) > 1:
            print(f"File name {file_name} is not unique")
            return None
        return download_file_by_id(files[0]["id"])
    else:
        print("No file id and no file name provided")
        return None


def download_file_by_id(file_id):
    service = get_drive_service()
    request = service.files().get_media(fileId=file_id)
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    done = False

    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%")

    return file.getvalue()


def delete_file(file_id=None, file_name=None):
    if file_id:
        return delete_file_by_id(file_id)
    elif file_name:
        files = search_file(file_name)
        if not files:
            print(f"Could not find file {file_name}")
            return False
        if len(files) > 1:
            print(f"File name {file_name} is not unique")
            return False
        return delete_file_by_id(files[0]["id"])
    else:
        print("No file id and no file name provided")
        return False


def delete_file_by_id(file_id):
    try:
        service = get_drive_service()
        service.files().delete(fileId=file_id).execute()
        print(f"File {file_id} deleted successfully.")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def upload_file(file_name, file_path, mime_type=None, parent_folder_id=None):
    service = get_drive_service()
    file_metadata = {'name': file_name}
    if parent_folder_id:
        file_metadata['parents'] = [parent_folder_id]

    media = MediaFileUpload(file_path, mimetype=mime_type)
    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        print(f"File {file_name} uploaded successfully. File ID: {file.get('id')}")
        return file.get('id')
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

