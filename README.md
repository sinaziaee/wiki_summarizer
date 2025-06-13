# Wiki Summary Application

This repository contains a backend API powered by FastAPI and a Streamlit frontend that fetches and summarizes Wikipedia articles using the OpenAI GPT model.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Running the Backend](#running-the-backend)
  - [Running the Frontend](#running-the-frontend)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- Scrape Wikipedia pages for a given query.
- Summarize articles using GPT-4o-mini up to 300 words.
- Simple UI with Streamlit.

## Prerequisites

- Python 3.10+ (preferably 3.11)
- Pip

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the root directory with the following content:

```env
OPENAI_API_KEY=your_openai_api_key
```

Optionally, set the backend URL for the frontend (if different from default):

```env
BACKEND_URL=http://localhost:8000
```

## Usage

### Running the Backend

From the root directory, start the FastAPI server with Uvicorn:

```bash
uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

### Running the Frontend

From the root directory, launch the Streamlit app:

```bash
streamlit run frontend/main.py
```

Navigate to the URL displayed in your terminal (e.g., `http://localhost:8501`).

## API Endpoints

- **GET** `/health`\
  Health check endpoint. Returns:

  ```json
  {"status": "ok"}
  ```

- **POST** `/summarize`\
  Summarize a Wikipedia article based on a search query.

  **Request Body:**

  ```json
  {
    "query": "Your search term"
  }
  ```

  **Response Body:**

  ```json
  {
    "query": "Your search term",
    "summary": "Summarized text...",
    "source_url": "https://en.wikipedia.org/wiki/..."
  }
  ```

## Project Structure

```
├── backend
│   ├── api.py           # FastAPI application
│   ├── scraper.py       # Wikipedia scraping utilities
│   └── summarizer.py    # OpenAI summarization logic
├── frontend
│   └── main.py          # Streamlit UI
├── requirements.txt     # Python dependencies
└── README.md            # Project overview and instructions
```

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for improvements.

## License

This project is licensed under the MIT License. Feel free to use and modify.

