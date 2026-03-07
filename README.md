# Family System

A web application that uses facial recognition and AI to predict family resemblances. Upload photos of parents to find the most similar children in the database, powered by [InsightFace](https://github.com/deepinsight/insightface) and a React + Flask stack.

## Features

- Upload mother and father photos via a React frontend
- AI-powered facial embedding comparison using InsightFace and OpenCV
- Weighted similarity search across a children database
- REST API built with Flask and Flask-CORS
- Responsive UI served from the Flask application

## Project Structure

```
family-system/
├── app.py                 # Flask application entry point
├── family_system.py       # FamilyMatcher core logic (facial embeddings)
├── sql.py                 # Database helpers
├── requirements.txt       # Python dependencies
├── package.json           # Node.js / SASS dependencies
├── frontend/              # React frontend source
├── templates/             # HTML templates
│   ├── index.html
│   └── results.html
├── children_db/           # Children image database
├── archive/               # Archived files
└── .github/               # GitHub templates and workflows
```

## Prerequisites

- Python 3.9+
- Node.js 16+ and npm
- A C++ build toolchain (required by `insightface` / `onnxruntime`)

## Setup Instructions

### Backend Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # Linux / macOS
   source .venv/bin/activate
   # Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask development server:

   ```bash
   python app.py
   ```

### Frontend Setup

1. Install Node.js dependencies:

   ```bash
   npm install
   ```

2. Build the frontend assets (SASS compilation):

   ```bash
   npm run build   # or the appropriate script defined in package.json
   ```

## Development

| Service  | URL                     |
|----------|-------------------------|
| Backend  | <http://localhost:5000> |
| Frontend | Served via Flask at `/` |

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating you agree to abide by its terms.

## License

This project is licensed under the [MIT License](LICENSE).
