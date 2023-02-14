source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 3001 --workers 4