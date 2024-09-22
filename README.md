# Products Scraper

This project is a web scraper for dental products, built with FastAPI. It scrapes product information from a specified website and stores the data locally.

## Features

- Web scraping with proxy support
- FastAPI backend
- JSON storage for scraped data
- Console notifications
- Caching mechanism

## Prerequisites

- Python 3.7+
- pip

## Setup

1. Clone the repository

2. Create a `.env` file in the project root with the following content:
   ```
   BASE_URL=https://dentalstall.com/shop/page/{}/
   STATIC_TOKEN=token
   PAGE_LIMIT=1
   ```
   Replace `token` with your chosen authentication token.

3. Set up the project:
   ```
   make setup
   ```
   This creates a virtual environment and installs dependencies.

## Usage

1. Start the FastAPI app:
   ```
   make run
   ```

2. In a new terminal, trigger the scraping process:
   ```
   make api
   ```
   This sends a POST request to the `/scrape` endpoint with the token and page_limit from the `.env` file.

3. To change the `PAGE_LIMIT` for a specific run:
    ```
    make api PAGE_LIMIT=2
    ```

## Cleaning up

To remove the virtual environment and cache files:
```
make clean
```

## API Endpoints

- POST `/scrape`: Initiates the scraping process
  - Headers:
    - `token`: Authentication token (must match `STATIC_TOKEN` in `.env`)
  - Body:
    ```json
    {
      "page_limit": 1,
    }
    ```
