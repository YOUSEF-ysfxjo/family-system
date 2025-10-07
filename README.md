# Family System Application

A web application built with React frontend and Flask backend.

## Project Structure

```
hackathon-project/
├── backend/               # Backend (Flask)
│   ├── app/              # Application package
│   │   ├── __init__.py   # Application factory
│   │   └── routes.py     # Application routes
│   ├── tests/            # Test files
│   ├── requirements.txt  # Python dependencies
│   └── wsgi.py          # WSGI entry point
│
├── frontend/             # Frontend (React)
│   ├── public/           # Static files
│   ├── src/              # React source code
│   ├── .gitignore
│   ├── package.json
│   └── README.md
│
└── templates/            # HTML templates
    ├── base.html
    ├── index.html
    └── results.html
```

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Run the Flask development server:
   ```bash
   python wsgi.py
   ```

### Frontend Setup

1. Install Node.js dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

## Development

- Backend runs on `http://localhost:5000`
- Frontend runs on `http://localhost:3000`

## Deployment

For production deployment, you'll need to build the React app and serve it through the Flask server.
