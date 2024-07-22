# API-Drive

This FastAPI application is designed to interact with the [Google Drive](https://www.google.com/drive/) API and provides an API interface for managing files. Users can authenticate to their Google accounts via OAuth, view, search, add and delete files on their Google Drives.


## Libraries Used

- [**FastAPI**](https://fastapi.tiangolo.com/)
- [**Google API Client Libraries**](https://github.com/googleapis/google-api-python-client)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/jenbefishy/Api-drive
    ```

2. Save the `client_secret` API key in `creds.json`.

3. Build the Docker image:
    ```bash
    docker build . -t api_drive
    ```

4. Run the Docker container:
    ```bash
    docker run -p 8000:8000 api_drive
    ```
