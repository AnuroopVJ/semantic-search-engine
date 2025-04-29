# Semantic Search Engine

A semantic web search engine that performs context-aware document retrieval using ChromaDB for vector storage, SQLAlchemy for structured metadata storage, and Streamlit for the user interface.

---

## What this is

This project implements a **semantic search engine** that goes beyond basic keyword search. It understands the meaning behind your queries and returns the most relevant documents from a crawled dataset.

---

## 📁 Project Structure

| File / Folder                  | Description                                                                                                  |
|--------------------------------|--------------------------------------------------------------------------------------------------------------|
| `Semantic_Search_Engine.ipynb` | Notebook with the full pipeline: crawling, vectorizing, launching UI, and tunneling (via `npx localtunnel`). |
| `crawler_vector.py`            | Python script to crawl and index webpages ethically.                                                         |
| `streamlit_ui.py`              | Streamlit-based semantic search interface.                                                                   |
| `requirements.txt`             | Required Python packages.                                                                                    |

---

## Features

- **Semantic Understanding**: Retrieves results based on meaning, not just keywords.
- **Ethical Crawler**:
  - Respects `robots.txt`
  - Includes delay between requests
  - Uses custom `User-Agent` to avoid overloading servers
- **Storage**:
  - Stores crawled data (title, description, URL) in SQLite
  - Stores document vectors in ChromaDB
- **Streamlit UI**:
  - Provides a simple interface to enter queries and view semantic results
  - Tunneling supported via `npx localtunnel` (especially for Colab environments)

---

## 🔧 Setup

### 1. Clone the repository

```bash
git clone https://github.com/AnuroopVJ/semantic-search-engine.git
cd semantic-search-engine
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## How the Crawler Works

Run the crawler via:

```bash
python crawler_vector.py
```

What it does:

- Crawls pages from a user-defined seed URL
- Checks `robots.txt` before scraping
- Waits between requests to avoid server overload
- Extracts and stores:
  - `title`
  - `description`
  - `URL`  
- Stores them in a local SQLite database (`crawled_sites.db`)
- Generates semantic embeddings and stores them in ChromaDB

---

## 📓 Jupyter Notebook (One-stop Pipeline)

You can run everything — crawling, vectorization, launching UI — from the `Semantic_Search_Engine.ipynb`.

### ⚠️ If running on Google Colab:

Since Colab doesn't allow direct access to localhost:

1. Make sure `npx` is available:
   ```bash
   !npm install -g localtunnel
   ```

2. Run Streamlit app from within the notebook:
   ```bash
   !streamlit run streamlit_ui.py &
   ```

3. Tunnel using:
   ```bash
   !npx localtunnel --port 8501
   ```

Copy the URL printed by localtunnel and open it in your browser to access the app.

---

## ▶️ Running Locally

```bash
python crawler_vector.py       # First, crawl and build the DB
streamlit run streamlit_ui.py # Then launch the UI
```

Visit `http://localhost:8501`.

---

## 📦 Dependencies

- `beautifulsoup4`
- `chromadb`
- `sqlalchemy`
- `streamlit`
- `requests`, etc.
- If using tunneling in notebooks: `node`, `npm`, and `localtunnel`

Install everything with:

```bash
pip install -r requirements.txt
```

---

## 🙌 Contributing

Pull requests and feature suggestions are welcome.

---

## 📄 License

MIT License © [Anuroop V J](https://github.com/AnuroopVJ)
