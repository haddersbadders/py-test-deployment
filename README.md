# Streamlit Google Sheets Dashboard

A minimal Streamlit application that connects to a Google Sheet using service account credentials and displays the data in an interactive table.

## Features
- Connects securely via Google Service Account credentials (no local JSON files).
- Displays data in a searchable table.
- Supports manual refresh button to bypass caching.
- Production-ready Dockerfile and Docker Compose configuration.

## Deployment on a Linux Server

Follow these instructions to build and run the application using Docker.

### 1. Prerequisites
Ensure you have Docker and Docker Compose installed on your server.
```bash
# Check if installed
docker --version
docker-compose --version
```

### 2. Configuration
Create a `.env` file from the provided example and populate it with your Google Cloud Service Account credentials and your target Spreadsheet URL.

```bash
cp .env.example .env
nano .env # Edit the file with your keys
```

**Important**: Make sure your Google Cloud Service account email (found in `GCP_CLIENT_EMAIL`) has been added as a "Viewer" to the Google Sheet you intend to read!

### 3. Build and Run
Use Docker Compose to build the image and start the container in detached mode.

```bash
# Build and start the container
docker-compose up -d --build

# Check the logs if needed
docker-compose logs -f
```

The application will be available at `http://<your-server-ip>:8501`.

### 4. Stopping the App
To stop the application:
```bash
docker-compose down
```
